# AIWorker/promptGen/nlp_analyzer.py
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from WebServer.Persistence.Models import Prompt as DBPrompt
from WebServer.Persistence.Models import Report as DBReport
from WebServer.Persistence.Models import UserLanguage as DBUserLanguage
from WebServer.Persistence.Models import UserMessage as DBUserMessage

# This code assumes you have a NormalizerPipeline class with a 'process(text)' method that returns analysis dict.
try:
    from AIWorker.nlp.normalizerPipeline import NormalizerPipeline
except Exception:
    NormalizerPipeline = None


class NLPAnalyzer:
    """Runs NLP normalization/analysis and stores user messages and reports."""

    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.normalizer = NormalizerPipeline() if NormalizerPipeline is not None else None

    async def analyze_and_store(
        self,
        user_id: int,
        prompt_id: int,
        raw_text: str,
    ) -> dict[str, Any]:
        """- stores UserMessage row
        - runs NLP analysis to produce a report JSON
        - stores Report row linking to the message
        - returns analysis dict
        """
        async with self.session_factory() as session:  # type: ignore # type: AsyncSession
            content_json = {"text": raw_text}
            stmt_insert = (
                insert(DBUserMessage)
                .values(
                    user_id=user_id,
                    prompt_id=prompt_id,
                    content=content_json,
                )
                .returning(DBUserMessage.id)
            )
            result = await session.execute(stmt_insert)
            message_id = result.scalar_one()
            await session.commit()

            analysis: dict[str, Any] = {"text": raw_text}

            if self.normalizer:
                try:
                    analysis_result = self.normalizer.process(raw_text)
                    analysis["analysis"] = analysis_result
                except Exception as e:
                    analysis["analysis_error"] = str(e)

            # 3) Create a Report entry (you can refine rating logic later)
            # default rating: None (or compute based on heuristics)
            report_content = {"analysis": analysis.get("analysis")}
            stmt_report = (
                insert(DBReport)
                .values(
                    user_id=user_id,
                    language_id=await self._get_user_language_id(session, user_id, prompt_id),
                    user_message_id=message_id,
                    content=report_content,
                    rating=None,
                    created_at=datetime.utcnow(),
                )
                .returning(DBReport.id)
            )

            rpt_res = await session.execute(stmt_report)
            report_id = rpt_res.scalar_one()
            await session.commit()

            return {"message_id": message_id, "report_id": report_id, "analysis": analysis}

    async def _get_user_language_id(
        self, session: AsyncSession, user_id: int, prompt_id: int
    ) -> int | None:
        """Best-effort resolution:
        - find language_id from prompt
        - check if user has UserLanguage linking that language
        - else return prompt.language_id
        """
        stmt_prompt = select(DBPrompt).where(DBPrompt.id == prompt_id)
        prompt_row = (await session.execute(stmt_prompt)).scalar_one_or_none()
        if not prompt_row:
            return None
        prompt_lang_id = prompt_row.language_id

        stmt_ul = (
            select(DBUserLanguage)
            .where(
                (DBUserLanguage.user_id == user_id)
                & (DBUserLanguage.language_id == prompt_lang_id),
            )
            .limit(1)
        )
        ul = (await session.execute(stmt_ul)).scalar_one_or_none()
        if ul:
            return ul.language_id
        return prompt_lang_id
