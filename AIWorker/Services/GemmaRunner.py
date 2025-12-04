import asyncio
from Classes import GemmaReviewer, InferenceRequest, GemmaTimeoutError, GemmaGenerationError
from dotenv import load_dotenv
from tenacity import stop_after_attempt, wait_exponential, retry_if_exception_type, retry
import os

load_dotenv()

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=8),
    retry=retry_if_exception_type((GemmaTimeoutError, GemmaGenerationError)),
    reraise=True
)
async def basic_inference(request: InferenceRequest) -> str:
    timeout = float(os.getenv("gemma_timeout", 300))
    reviewer = GemmaReviewer() 

    try:
        return await asyncio.wait_for(
            asyncio.to_thread(
                reviewer.infere_basic_text,
                request.text,
                request.user_lvl,
                request.user_language,
                request.prompt
            ),
            timeout=timeout
        )

    except asyncio.TimeoutError as exc:
        raise GemmaTimeoutError(f"LLM inference exceeded {timeout}s") from exc
