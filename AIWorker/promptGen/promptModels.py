from dataclasses import dataclass
from typing import Optional

from AIWorker.promptGen.promptEnums import PromptCategory, PromptDifficulty, UnifiedPromptType


@dataclass
class PromptRequest:
    prompt_difficulty: PromptDifficulty
    prompt_type: UnifiedPromptType
    user_language: str                # language code or name (lowercased)
    current_level: str                # CEFR e.g. "A1"
    target_level: str
    category: PromptCategory = PromptCategory.GENERAL
    topic: Optional[str] = None


@dataclass
class PromptResponse:
    prompt_text: str
    source: str        # "internal", "database", or "llm"
    prompt_id: Optional[int] = None
