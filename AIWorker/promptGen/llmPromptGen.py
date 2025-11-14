from AIWorker.promptGen.promptModels import PromptRequest

# TODO: integrate with LLM client (OpenAI, OpenRouter, Local LLM, etc.)


class LLMPromptGenerator:
    """Tier 3: LLM fallback. Replace generate() with your OpenAI/OpenRouter/Local LLM call.
    Kept intentionally minimal and sync/async-agnostic so you can plug any client.
    """

    async def generate(self, request: PromptRequest) -> str:
        # Example scaffold: craft a strong instruction for your LLM client
        instruction = (
            f"Create a {request.prompt_difficulty.value} language prompt in "
            f"{request.user_language} targeted at level {request.current_level}."
        )
        if request.topic:
            instruction += f" Topic: {request.topic}."
        instruction += " Provide a single short prompt (1-2 sentences)."

        return instruction
