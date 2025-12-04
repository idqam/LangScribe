from fastapi import APIRouter, status, HTTPException
from Repositories import create_report
from Persistence.DTOs import ReportCreate
from Resources import lifespan
from fastapi_cache import FastAPICache
from Persistence.Enums import RATE
import json

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)

@router.post('/jobs/{job_id}')
async def process_jobs(job_id: int, txt: str):

    context_json = await FastAPICache.get_backend().get(f"job_context:{job_id}")
    
    if not context_json:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job context not found for job_id: {job_id}"
        )
    
    context = json.loads(context_json)

    report = ReportCreate(
        user_id=context["user_id"],
        language_id=context["language_id"],
        user_message_id=context["user_message_id"],
        content=txt,
        rating=RATE.EXPERT
    )
    
    create_report(report)
    
    await FastAPICache.get_backend().delete(f"job_context:{job_id}")
    
    return {"status": "accepted", "job_id": job_id}