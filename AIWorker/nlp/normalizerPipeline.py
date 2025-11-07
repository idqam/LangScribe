from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from AIWorker.nlp.models import SentenceSegmentationResult, UserInput
from AIWorker.nlp.textNormalizer import TextNormalizer


class NormalizerPipeline:
    """Factory pipeline for selecting and executing the correct TextNormalizer.

    Automatically selects a language-appropriate normalizer,
    handles multi-block user input, and returns a SentenceSegmentationResult
    skeleton with normalized text and metadata.
    """

    def __init__(self) -> None:
        """Initialize and cache supported normalizers."""
        self.normalizers: dict[str, TextNormalizer] = {
            "en": TextNormalizer(language="en"),
            "es": TextNormalizer(language="es"),
        }
        self.default_normalizer = TextNormalizer(language="en")

    def process_user_input(self, user_input: UserInput) -> SentenceSegmentationResult:
        """Normalize text blocks and return a structured result."""
        language = user_input.language or "en"
        prompt_type = user_input.prompt_type
        normalizer = self._select_normalizer(language)

        normalized_blocks: list[str] = []
        aggregated_metadata: dict[str, Any] = {
            "placeholders": {"urls": 0, "emails": 0, "emojis": 0, "numbers": 0},
            "noise_ratio_avg": 0.0,
            "punctuation_total": 0,
        }

        for block in user_input.text:
            normalized_text, metadata = normalizer.normalize(block)
            normalized_blocks.append(normalized_text)

            ph = metadata.get("placeholders", {})
            for key, value in ph.items():
                aggregated_metadata["placeholders"][key] += int(value)

            aggregated_metadata["noise_ratio_avg"] += float(metadata.get("noise_ratio", 0.0))
            aggregated_metadata["punctuation_total"] += int(metadata.get("punctuation_count", 0))

        num_blocks = max(len(user_input.text), 1)
        aggregated_metadata["noise_ratio_avg"] = round(
            aggregated_metadata["noise_ratio_avg"] / num_blocks,
            3,
        )

        full_normalized_text = "\n\n".join(normalized_blocks)

        return SentenceSegmentationResult(
            original_text="\n\n".join(user_input.text),
            normalized_text=full_normalized_text,
            language=language,
            prompt_type=prompt_type,
            processing_timestamp=datetime.now(UTC),
            sentences=[],
            token_count=0,
            sentence_count=0,
            document_complexity=None,
            grammar_errors=[],
            parser_used="TextNormalizer v1",
            notes=f"Processed {num_blocks} blocks. Metadata: {aggregated_metadata}",
        )

    def _select_normalizer(self, language: str) -> TextNormalizer:
        """Return a language-specific normalizer if available."""
        if language in self.normalizers:
            return self.normalizers[language]
        if self._is_non_latin_language(language):
            return TextNormalizer(language=language)
        return self.default_normalizer

    def _is_non_latin_language(self, language: str) -> bool:
        """Determine if language uses a non-Latin script (extendable)."""
        non_latin_langs = {"zh", "ja", "ko", "ar", "ru", "hi"}
        return language.lower() in non_latin_langs
