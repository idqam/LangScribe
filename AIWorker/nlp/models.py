from datetime import datetime

from pydantic import BaseModel, Field


# ---------- USER INPUT ----------
class UserInput(BaseModel):
    text: list[str] = Field(..., description="List of text blocks or paragraphs to analyze.")
    language: str | None = Field(
        None,
        description="ISO code of the input language (e.g., 'en', 'es').",
    )
    prompt_type: str | None = Field(
        None,
        description="Type or topic of the prompt (e.g., 'diary', 'academic').",
    )
    prompt: str | None = Field(None, description="The original prompt given to the user.")


# ---------- TOKEN-LEVEL STRUCTURE ----------
class Token(BaseModel):
    token: str
    lemma: str | None = None
    pos: str | None = None
    dep: str | None = None
    head: str | None = None
    index: int | None = None

    # Extended fields for robustness and future metrics
    char_start: int | None = None
    char_end: int | None = None
    token_type: str | None = Field(
        None,
        description="word, punctuation, url, emoji, number, etc.",
    )
    is_stopword: bool | None = None
    frequency_rank: int | None = Field(None, description="Frequency rank in reference corpus.")


# ---------- POS GROUPING ----------
class POSCounts(BaseModel):
    nouns: int = 0
    verbs: int = 0
    adjectives: int = 0
    adverbs: int = 0
    pronouns: int = 0
    conjunctions: int = 0
    determiners: int = 0
    prepositions: int = 0
    others: int = 0

    # Additional linguistic/syntactic counts
    passive_voice_count: int = 0
    relative_clause_count: int = 0
    subordinate_clause_count: int = 0
    punctuation_counts: dict[str, int] | None = None


# ---------- GRAMMAR ERROR MODEL ----------
class GrammarError(BaseModel):
    error_type: str
    start_idx: int | None = None
    end_idx: int | None = None
    suggestion: str | None = None
    confidence: float | None = None


# ---------- SENTENCE STRUCTURE ----------
class Sentence(BaseModel):
    id: int
    text: str
    start_idx: int | None = None
    end_idx: int | None = None
    char_start: int | None = None
    char_end: int | None = None

    tokens: list[Token] | None = None
    pos_counts: POSCounts | None = None
    unique_pos: int | None = None
    punctuation_variety: int | None = None

    # Complexity + interpretability
    complexity_score: float | None = None  # Normalized 0–1 or 0–100
    complexity_components: dict[str, float] | None = (
        None  # e.g., {"length": 0.3, "clause_depth": 0.4}
    )
    length_in_tokens: int | None = None
    clause_depth: float | None = None
    parse_confidence: float | None = None
    confidence: float | None = None  # sentence-level metric reliability

    # Additional metadata & diagnostics
    sentence_flags: list[str] | None = Field(
        None,
        description="e.g., ['fragment', 'run_on', 'quotation']",
    )
    entity_mentions_count: int | None = None
    sensitive_content_flag: bool | None = None
    errors: list[GrammarError] | None = None


# ---------- DOCUMENT-LEVEL STRUCTURE ----------
class DocumentComplexity(BaseModel):
    avg_complexity: float
    total_sentences: int
    normalized_complexity: float | None = None
    document_confidence: float | None = None
    weighting_scheme: dict[str, float] | None = (
        None  # e.g., weights for length, syntax, lexical diversity
    )
    aggregation_method: str | None = Field(
        "median",
        description="Method used for aggregation (mean, median, etc.)",
    )


class SentenceSegmentationResult(BaseModel):
    original_text: str | None = None
    normalized_text: str | None = None
    language: str | None = None
    prompt_type: str | None = None
    processing_timestamp: datetime = Field(default_factory=datetime.utcnow)

    sentences: list[Sentence]
    document_complexity: DocumentComplexity | None = None
    grammar_errors: list[GrammarError] | None = None

    # Higher-level metadata
    token_count: int | None = None
    sentence_count: int | None = None
    parser_used: str | None = None
    notes: str | None = Field(None, description="General processing notes or pipeline metadata.")
