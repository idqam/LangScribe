from fastapi import FastAPI, status, Request,Body
from Classes import InferenceRequest, InferenceReturn
from Services import basic_inference
from Classes import GemmaError,GemmaTimeoutError,GemmaGenerationError, GemmaReviewer
import httpx
import asyncio

app = FastAPI(title="AIWorker Service")

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "feedback-service"}


@app.post('/test')
async def test(request: InferenceRequest):
    print("Request received!")
    return await GemmaReviewer().infere_basic_text(**request.model_dump())


@app.post('/jobs/{job_id}')
async def post_message(webserver_request: InferenceRequest, job_id: int):


    
    async def create_job(webserver_request: InferenceRequest, job_id: int):
        try:
            llm_response = await basic_inference(webserver_request)

            webserver_response = InferenceReturn(
                job_id=job_id,
                llm_response=llm_response
            )

            async with httpx.AsyncClient() as client:
                await client.post(
                    url=f"http://web-server:8000/jobs/{job_id}",
                    json=webserver_response.model_dump()
                )

        except GemmaGenerationError:
            print(f"Gemma failed to generate response on job {job_id}")
        except GemmaTimeoutError:
            print(f"Gemma timed out response on job {job_id}")
        except GemmaError:
            print("Gemma Errored!")
            raise
        except Exception as e:
            print(f"Background task failed: {e}")

    asyncio.create_task(create_job(webserver_request, job_id))

    return {"status": "accepted", "job_id": job_id}
