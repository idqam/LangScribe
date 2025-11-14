from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from AIWorker.promptGen.promptEnums import PromptDifficulty, PromptCategory
from WebServer.Persistence.Models import Prompt as DBPrompt, Language as DBLanguage


class PromptRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_random_prompt_text(
        self,
        language: str,
        level: str,
        difficulty: PromptDifficulty,
        category: PromptCategory
    ) -> Optional[str]:
        normalized_lang = language.strip().lower()
        normalized_level = level.strip().upper()

        async with self.session_factory() as session:
            lang_stmt = select(DBLanguage).where(
                (DBLanguage.code == normalized_lang.upper())
                | (DBLanguage.name.ilike(normalized_lang))
            ).limit(1)

            lang_row = (await session.execute(lang_stmt)).scalar_one_or_none()
            if not lang_row:
                return None

            stmt = (
                select(DBPrompt)
                .where(DBPrompt.language_id == lang_row.id)
                .where(DBPrompt.level == normalized_level)
                .where(DBPrompt.difficulty == difficulty.name)
                .where(DBPrompt.category == category.name)
                .order_by(func.random())
                .limit(1)
            )

            result = (await session.execute(stmt)).scalar_one_or_none()
            if not result:
                return None

            content = result.content or {}
            return content.get("text") or content.get("prompt")

    async def get_prompts_for_language_level(self, language: str, level: str):
        normalized_lang = language.strip().lower()
        normalized_level = level.strip().upper()

        async with self.session_factory() as session:
            lang_stmt = select(DBLanguage).where(
                (DBLanguage.code == normalized_lang.upper())
                | (DBLanguage.name.ilike(normalized_lang))
            ).limit(1)

            lang_row = (await session.execute(lang_stmt)).scalar_one_or_none()
            if not lang_row:
                return []

            stmt = (
                select(DBPrompt)
                .where(DBPrompt.language_id == lang_row.id)
                .where(DBPrompt.level == normalized_level)
            )

            return (await session.execute(stmt)).scalars().all()

    async def insert_prompt(self, prompt: DBPrompt):
        async with self.session_factory() as session:
            session.add(prompt)
            await session.commit()
            return prompt
