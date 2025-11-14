from typing import Optional

from AIWorker.promptGen.llmPromptGen import LLMPromptGenerator as LLMGenerator
from AIWorker.promptGen.promptEnums import PromptCategory, PromptDifficulty
from AIWorker.promptGen.promptRegistry import PromptRegistry
from AIWorker.promptGen.promptRepository import PromptRepository


class PromptPipeline:
    def __init__(
        self,
        registry: PromptRegistry,
        repository: PromptRepository,
        llm_generator: LLMGenerator,
    ):
        self.registry = registry
        self.repository = repository
        self.llm = llm_generator

    async def get_daily_prompt(
        self,
        user_id: str,
        language: str,
        level: str,
        category: PromptCategory = PromptCategory.GENERAL,
        difficulty: PromptDifficulty = PromptDifficulty.MEDIUM,
    ) -> str:
        cached = self.registry.get_cached_prompt(user_id, language, level)
        if cached:
            return cached

        db_prompt = await self.repository.get_random_prompt_text(
            language=language,
            level=level,
            difficulty=difficulty,
            category=category,
        )
        if db_prompt:
            self.registry.store_prompt(user_id, language, level, db_prompt)
            return db_prompt

        request = {
            "language": language,
            "level": level,
            "difficulty": difficulty,
            "category": category,
            "count": 1,
        }
        generated = await self.llm.generate(request)  # type: ignore

        prompt_text = generated[0]
        # await self.llm.persist_prompts(self.repository, language, level, difficulty, category, generated)

        self.registry.store_prompt(user_id, language, level, prompt_text)
        return prompt_text

    async def preload_missing_prompts(
        self,
        language: str,
        level: str,
        category: PromptCategory,
        difficulty: PromptDifficulty,
        count: int,
    ):
        existing = await self.repository.get_prompts_for_language_level(language, level)
        if len(existing) >= count:
            return

        request = {
            "language": language,
            "level": level,
            "difficulty": difficulty,
            "category": category,
            "count": 1,
        }
        generated = await self.llm.generate(request)  # type: ignore
        # await self.llm.persist_prompts(
        #     repository=self.repository,
        #     language=language,
        #     level=level,
        #     difficulty=difficulty,
        #     category=category,
        #     prompts=generated
        # )
