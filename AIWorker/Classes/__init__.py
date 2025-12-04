from .Gemma import GemmaReviewer
from .request_dtos import InferenceRequest, InferenceReturn
from .CustomExceptions import (
    GemmaError,
    GemmaGenerationError,
    GemmaTimeoutError
)

Singleton = GemmaReviewer()