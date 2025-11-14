from enum import Enum
from typing import Dict, List, Optional
import random

from AIWorker.promptGen.promptEnums import PromptDifficulty, UnifiedPromptType


class PromptRequest:
    def __init__(
        self,
        prompt_difficulty: PromptDifficulty,
        prompt_type: UnifiedPromptType,
        user_language: str,
        current_level: str,
        target_level: str,
        topic: Optional[str] = None,
    ):
        self.prompt_type = prompt_type
        self.prompt_difficulty = prompt_difficulty
        self.user_language = user_language
        self.current_level = current_level
        self.target_level = target_level
        self.topic = topic

    def to_dict(self) -> dict:
        return {
            "prompt_difficulty": self.prompt_difficulty.value,
            "prompt_type": self.prompt_type.value,
            "user_language": self.user_language,
            "current_level": self.current_level,
            "target_level": self.target_level,
            "topic": self.topic,
        }


class PromptResponse:
    def __init__(
        self,
        prompt_id: str,
        text: str,
        language: str,
        level: str,
        category: str,
        difficulty: str,
        complexity: str,
        unified_type: str,
    ):
        self.prompt_id = prompt_id
        self.text = text
        self.language = language
        self.level = level
        self.category = category
        self.difficulty = difficulty
        self.complexity = complexity
        self.unified_type = unified_type

    def to_dict(self):
        return {
            "prompt_id": self.prompt_id,
            "text": self.text,
            "language": self.language,
            "level": self.level,
            "category": self.category,
            "difficulty": self.difficulty,
            "complexity": self.complexity,
            "unified_type": self.unified_type,
        }





class PromptSeed:
    """Represents one row of prompt_seeds in DB."""

    def __init__(
        self,
        id: str,
        language: str,
        level: str,
        difficulty: str,
        complexity: str,
        unified_type: str,
        category: str,
        topic: Optional[str],
        base_prompt: str,
    ):
        self.id = id
        self.language = language
        self.level = level
        self.difficulty = difficulty
        self.complexity = complexity
        self.unified_type = unified_type
        self.category = category
        self.topic = topic
        self.base_prompt = base_prompt



class PromptRegistry:
    """
    Loads all prompts at startup and organizes them by:
    registry[language][level] -> List[PromptSeed]
    """

    def __init__(self):
        self.registry: Dict[str, Dict[str, List[PromptSeed]]] = {}
        self.cache: Dict[str, PromptSeed] = {}  # (language+level)->cached prompt

 
    def load_from_db(self, seeds: List[PromptSeed]):
        for seed in seeds:
            lang = seed.language.lower()
            level = seed.level.upper()

            if lang not in self.registry:
                self.registry[lang] = {}

            if level not in self.registry[lang]:
                self.registry[lang][level] = []

            self.registry[lang][level].append(seed)

    
    def get_prompt(self, language: str, level: str) -> Optional[PromptSeed]:
        lang = language.lower()
        level = level.upper()

        key = f"{lang}:{level}"

        
        if key in self.cache:
            return self.cache[key]

        
        if lang not in self.registry or level not in self.registry[lang]:
            return None

        options = self.registry[lang][level]

        if not options:
            return None

        
        selected = random.choice(options)

        
        self.cache[key] = selected

        return selected



class PromptGenerator:
    def __init__(self, registry: PromptRegistry):
        self.registry = registry

    # ---------------------
    # MAIN GENERATION METHOD
    # ---------------------
    def generate(self, request: PromptRequest) -> PromptResponse:
        
        seed = self.registry.get_prompt(request.user_language, request.current_level)

        if seed is None:
            raise ValueError("No prompts available for this language/level.")

        return PromptResponse(
            prompt_id=seed.id,
            text=seed.base_prompt,
            language=seed.language,
            level=seed.level,
            category=seed.category,
            difficulty=seed.difficulty,
            complexity=seed.complexity,
            unified_type=seed.unified_type,
        )

    # ---------------------
    # MANUAL DB LOOKUP
    # ---------------------
    def get_prompt_text_from_db(self, prompt_id: str) -> str:
        # placeholder; replace with actual DB call
        return "Sample prompt text from DB."
