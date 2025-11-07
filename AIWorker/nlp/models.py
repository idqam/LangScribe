from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


# ---------- USER INPUT ----------
class UserInput(BaseModel):
    text: List[str] = Field(..., description="List of text blocks or paragraphs to analyze.")
    language: Optional[str] = Field(None, description="ISO code of the input language (e.g., 'en', 'es').")
    prompt_type: Optional[str] = Field(None, description="Type or topic of the prompt (e.g., 'diary', 'academic').")


# ---------- TOKEN-LEVEL STRUCTURE ----------
class Token(BaseModel):
    token: str
    lemma: Optional[str] = None
    pos: Optional[str] = None
    dep: Optional[str] = None
    head: Optional[str] = None
    index: Optional[int] = None

    # Extended fields for robustness and future metrics
    char_start: Optional[int] = None
    char_end: Optional[int] = None
    token_type: Optional[str] = Field(None, description="word, punctuation, url, emoji, number, etc.")
    is_stopword: Optional[bool] = None
    frequency_rank: Optional[int] = Field(None, description="Frequency rank in reference corpus.")


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
    punctuation_counts: Optional[Dict[str, int]] = None


# ---------- GRAMMAR ERROR MODEL ----------
class GrammarError(BaseModel):
    error_type: str
    start_idx: Optional[int] = None
    end_idx: Optional[int] = None
    suggestion: Optional[str] = None
    confidence: Optional[float] = None


# ---------- SENTENCE STRUCTURE ----------
class Sentence(BaseModel):
    id: int
    text: str
    start_idx: Optional[int] = None
    end_idx: Optional[int] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None

    tokens: Optional[List[Token]] = None
    pos_counts: Optional[POSCounts] = None
    unique_pos: Optional[int] = None
    punctuation_variety: Optional[int] = None

    # Complexity + interpretability
    complexity_score: Optional[float] = None  # Normalized 0–1 or 0–100
    complexity_components: Optional[Dict[str, float]] = None  # e.g., {"length": 0.3, "clause_depth": 0.4}
    length_in_tokens: Optional[int] = None
    clause_depth: Optional[float] = None
    parse_confidence: Optional[float] = None
    confidence: Optional[float] = None  # sentence-level metric reliability

    # Additional metadata & diagnostics
    sentence_flags: Optional[List[str]] = Field(None, description="e.g., ['fragment', 'run_on', 'quotation']")
    entity_mentions_count: Optional[int] = None
    sensitive_content_flag: Optional[bool] = None
    errors: Optional[List[GrammarError]] = None


# ---------- DOCUMENT-LEVEL STRUCTURE ----------
class DocumentComplexity(BaseModel):
    avg_complexity: float
    total_sentences: int
    normalized_complexity: Optional[float] = None
    document_confidence: Optional[float] = None
    weighting_scheme: Optional[Dict[str, float]] = None  # e.g., weights for length, syntax, lexical diversity
    aggregation_method: Optional[str] = Field("median", description="Method used for aggregation (mean, median, etc.)")


class SentenceSegmentationResult(BaseModel):
    original_text: Optional[str] = None
    normalized_text: Optional[str] = None
    language: Optional[str] = None
    prompt_type: Optional[str] = None
    processing_timestamp: datetime = Field(default_factory=datetime.utcnow)

    sentences: List[Sentence]
    document_complexity: Optional[DocumentComplexity] = None
    grammar_errors: Optional[List[GrammarError]] = None

    # Higher-level metadata
    token_count: Optional[int] = None
    sentence_count: Optional[int] = None
    parser_used: Optional[str] = None
    notes: Optional[str] = Field(None, description="General processing notes or pipeline metadata.")
