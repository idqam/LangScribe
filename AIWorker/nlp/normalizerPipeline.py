from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from AIWorker.nlp.models import SentenceSegmentationResult, UserInput
from AIWorker.nlp.textNormalizer import TextNormalizer


class NormalizerPipeline:
    """Pipeline for selecting and applying the right TextNormalizer."""

    def __init__(self) -> None:
        self.normalizers: dict[str, TextNormalizer] = {
            "en": TextNormalizer(language="en"),
            "es": TextNormalizer(language="es"),
        }
        self.default_normalizer = TextNormalizer(language="en")

    def process_user_input(self, user_input: UserInput) -> SentenceSegmentationResult:
        """Normalize text blocks with spaCy integration."""
        language = user_input.language or "en"
        prompt_type = user_input.prompt_type
        normalizer = self._select_normalizer(language)

        normalized_blocks: list[str] = []
        all_sentences: list[str] = []
        aggregated_metadata: dict[str, Any] = {
            "placeholders": {"urls": 0, "emails": 0, "emojis": 0, "numbers": 0},
            "noise_ratio_avg": 0.0,
            "punctuation_total": 0,
            "token_total": 0,
            "sentence_total": 0,
        }

        for block in user_input.text:
            normalized_text, metadata = normalizer.normalize(block)
            normalized_blocks.append(normalized_text)

            for k, v in metadata["placeholders"].items():
                aggregated_metadata["placeholders"][k] += v

            aggregated_metadata["noise_ratio_avg"] += metadata["noise_ratio"]
            aggregated_metadata["punctuation_total"] += metadata["punctuation_count"]
            aggregated_metadata["token_total"] += metadata["token_count"]
            aggregated_metadata["sentence_total"] += metadata["sentence_count"]

            doc_sentences = normalizer.nlp(normalized_text).sents
            all_sentences.extend([s.text.strip() for s in doc_sentences])

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
            sentences=all_sentences,
            token_count=aggregated_metadata["token_total"],
            sentence_count=aggregated_metadata["sentence_total"],
            document_complexity=None,
            grammar_errors=[],
            parser_used="spaCy-powered TextNormalizer v2",
            notes=f"Processed {num_blocks} blocks with spaCy. Metadata: {aggregated_metadata}",
        )

    def _select_normalizer(self, language: str) -> TextNormalizer:
        """Return a language-specific normalizer if available."""
        return self.normalizers.get(language, self.default_normalizer)

    def process(self, raw_text: str) -> SentenceSegmentationResult:
        """Convenience wrapper so external systems can call pipeline.process(raw_text)
        instead of building a UserInput object manually.
        """
        user_input = UserInput(
            text=[raw_text],
            language=None,
            prompt_type=None,
            prompt=None,
        )
        return self.process_user_input(user_input)
