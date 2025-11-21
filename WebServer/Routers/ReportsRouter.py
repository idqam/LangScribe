from fastapi import APIRouter, HTTPException, status
from loguru import logger
from Persistence.DTOs import ReportCreate, ReportRead, ReportUpdate
from Repositories import (
    create_report,
    delete_report,
    get_all_reports,
    get_one_report,
    update_report,
)

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get("/", tags=["reports"], response_model=list[ReportRead])
async def read_reports() -> [ReportRead]:
    try:
        reports = await get_all_reports()
        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", tags=["reports"], response_model=ReportRead)
async def read_report(id: int) -> ReportRead:
    try:
        report = await get_one_report(id, email= None)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/",
    tags=["reports"],
    response_model=ReportRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_report(report_dto: ReportCreate) -> ReportRead:
    try:
        logger.error("router")
        report = await create_report(report_dto)
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/{id}", tags=["reports"], response_model=bool)
async def update_existing_report(id: int, report_dto: ReportUpdate):
    try:
        success = await update_report(id, report_dto)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{id}", tags=["reports"], response_model=bool)
async def delete_existing_report(id: int):

    try:
        success = await delete_report(id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
