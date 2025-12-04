class GemmaError(Exception):
    """Base class for Gemma model errors."""

class GemmaTimeoutError(GemmaError):
    """Raised when inference exceeds timeout."""

class GemmaGenerationError(GemmaError):
    """Raised when the model fails during generation."""
