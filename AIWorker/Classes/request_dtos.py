from pydantic import BaseModel

class InferenceRequest(BaseModel):
    text: str
    user_lvl: str
    user_language: str
    prompt: str

class InferenceReturn(BaseModel):
    job_id: int
    llm_response: str