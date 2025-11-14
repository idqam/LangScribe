# prompt_dao.py
from typing import Optional, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from WebServer.Persistence.Models import Prompt as DBPrompt, Language as DBLanguage
from AIWorker.promptGen.promptEnums import PromptDifficulty, PromptCategory

class PromptDAO:
    """
    Async DAO for prompt retrieval from the DB.
    Expects DBPrompt.content to be JSON containing 'text' or 'prompt' keys.
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_random_prompt_text(
        self,
        language: str,
        unified_type: str,
        difficulty: PromptDifficulty,
        category: PromptCategory
    ) -> Optional[str]:
        """
        Finds a random prompt by language and difficulty. The query is simple —
        expand filters as you store more metadata in DBPrompt.content.
        """

        async with self.session_factory() as session:  # type: ignore # type: AsyncSession
            stmt_lang = select(DBLanguage).where(
                (DBLanguage.code == language.upper()) | (DBLanguage.name.ilike(language))
            ).limit(1)
            lang_row = (await session.execute(stmt_lang)).scalar_one_or_none()
            if not lang_row:
                return None

            stmt = (
                select(DBPrompt)
                .where(DBPrompt.language_id == lang_row.id)
                .where(DBPrompt.difficulty == difficulty.name)
                .order_by(func.random())
                .limit(1)
            )
            row = (await session.execute(stmt)).scalar_one_or_none()
            if not row:
                return None

            content = row.content or {}
            text = content.get("text") or content.get("prompt") or content.get("base_prompt")
            return text
