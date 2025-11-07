from __future__ import annotations

import re
import unicodedata
from typing import Any

import spacy


class TextNormalizer:
    """Modular text normalization pipeline.

    Clean user text for robust segmentation and parsing
    while preserving linguistic and syntactic richness.
    """

    def __init__(self, language: str = "en") -> None:
        """Initialize a language-specific normalizer."""
        self.language = language
        self.nlp = self._load_language_model(language)

    def normalize(self, text: str) -> tuple[str, dict[str, Any]]:
        """Normalize input text while preserving syntactic information."""
        original_text = text
        metadata: dict[str, Any] = {}

        text = self._normalize_unicode(text)
        text = self._normalize_whitespace(text)
        text = self._normalize_punctuation(text)
        text, placeholders = self._replace_special_tokens(text)
        metadata["placeholders"] = placeholders
        metadata.update(self._compute_noise_metrics(original_text, text))

        if self.nlp is not None:
            text = self._ensure_sentence_spacing(text)

        metadata["normalized_length"] = len(text)
        metadata["language"] = self.language
        return text.strip(), metadata

    def _load_language_model(self, language: str) -> spacy.language.Language | None:
        """Safely attempt to load a blank spaCy model."""
        try:
            return spacy.blank(language)
        except Exception:  # noqa: BLE001
            return None

    def _normalize_unicode(self, text: str) -> str:
        """Normalize Unicode forms (quotes, dashes, ellipses)."""
        return unicodedata.normalize("NFKC", text)

    def _normalize_whitespace(self, text: str) -> str:
        """Collapse extra whitespace and remove invisible characters."""
        text = re.sub(r"\s+", " ", text)
        text = text.replace("\u200b", "")
        return text.strip()

    def _normalize_punctuation(self, text: str) -> str:
        """Standardize punctuation forms but keep semantic distinctions."""
        substitutions = {
            "\u201c": '"',
            "\u201d": '"',
            "\u2018": "'",
            "\u2019": "'",
            "\u2014": "-",
            "\u2013": "-",
            "\u2026": "...",
        }
        for old, new in substitutions.items():
            text = text.replace(old, new)
        return text

    def _replace_special_tokens(self, text: str) -> tuple[str, dict[str, int]]:
        """Replace URLs, emails, emojis, and numbers with placeholders."""
        placeholders = {
            "urls": len(re.findall(r"https?://\S+|www\.\S+", text)),
            "emails": len(re.findall(r"\S+@\S+", text)),
            "emojis": len(re.findall(r"[\U00010000-\U0010ffff]", text)),
            "numbers": len(re.findall(r"\b\d+(?:\.\d+)?\b", text)),
        }

        text = re.sub(r"https?://\S+|www\.\S+", "<URL>", text)
        text = re.sub(r"\S+@\S+", "<EMAIL>", text)
        text = re.sub(r"[\U00010000-\U0010ffff]", "<EMOJI>", text)
        text = re.sub(r"\b\d+(?:\.\d+)?\b", "<NUM>", text)

        return text, placeholders

    def _compute_noise_metrics(self, original: str, normalized: str) -> dict[str, Any]:
        """Compute ratio of placeholders and punctuation counts."""
        total_chars = max(len(original), 1)
        placeholder_count = normalized.count("<")
        punctuation_count = len(re.findall(r"[.,!?;:]", normalized))
        noise_ratio = placeholder_count / total_chars
        return {
            "noise_ratio": round(noise_ratio, 3),
            "punctuation_count": punctuation_count,
        }

    def _ensure_sentence_spacing(self, text: str) -> str:
        """Ensure spacing between tokens if spaCy is loaded."""
        if self.nlp is None:
            return text
        doc = self.nlp.make_doc(text)
        return " ".join(token.text for token in doc)
