from __future__ import annotations

import re
import unicodedata
from typing import Any

import spacy


class TextNormalizer:
    """Language-aware text normalization with spaCy integration."""

    def __init__(self, language: str = "en") -> None:
        self.language = language
        self.nlp = self._load_language_model(language)

    def normalize(self, text: str) -> tuple[str, dict[str, Any]]:
        """Normalize text with regex + spaCy tokenization."""
        original_text = text

        text = self._normalize_unicode(text)
        text = self._normalize_whitespace(text)
        text = self._normalize_punctuation(text)
        text, placeholders = self._replace_special_tokens(text)

        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]

        normalized_text = " ".join(token.text for token in doc)

        metadata: dict[str, Any] = {
            "placeholders": placeholders,
            "token_count": len(doc),
            "sentence_count": len(sentences),
            "punctuation_count": sum(1 for t in doc if t.is_punct),
            "noise_ratio": round(normalized_text.count("<") / max(len(original_text), 1), 3),
            "language": self.language,
        }

        return normalized_text.strip(), metadata

    def _load_language_model(self, language: str) -> spacy.language.Language:
        """Try loading full model, fallback to blank pipeline with sentencizer."""
        try:
            nlp = spacy.load(f"{language}_core_web_sm", disable=["ner"])
        except Exception:
            nlp = spacy.blank(language)

        # ✅ Always ensure a sentencizer exists for sentence segmentation
        if "parser" not in nlp.pipe_names and "senter" not in nlp.pipe_names:
            nlp.add_pipe("sentencizer")

        return nlp

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
