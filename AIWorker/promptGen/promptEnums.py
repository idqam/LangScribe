from enum import Enum


class PromptDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class PromptComplexity(Enum):
    SIMPLE = "simple"
    INTERMEDIATE = "intermediate"
    COMPLEX = "complex"


class UnifiedPromptType(Enum):
    EASY_SIMPLE = "easy_simple"
    EASY_INTERMEDIATE = "easy_intermediate"
    EASY_COMPLEX = "easy_complex"
    MEDIUM_SIMPLE = "medium_simple"
    MEDIUM_INTERMEDIATE = "medium_intermediate"
    MEDIUM_COMPLEX = "medium_complex"
    HARD_SIMPLE = "hard_simple"
    HARD_INTERMEDIATE = "hard_intermediate"
    HARD_COMPLEX = "hard_complex"


class PromptCategory(Enum):
    DAILY_LIFE = "daily_life"
    TRAVEL = "travel"
    CULTURE = "culture"
    OPINION = "opinion"
    STORY = "story"
    PROFESSIONAL = "professional"
    GENERAL = "general"
