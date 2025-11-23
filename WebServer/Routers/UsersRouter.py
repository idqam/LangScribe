from fastapi import APIRouter, Depends, HTTPException, status
from Persistence.DTOs import LanguageRead, ReportRead, UserCreate, UserRead, UserUpdate
from Repositories import delete_user, get_languages, get_one_user, get_reports, update_user
from Resources import verify_token

router = APIRouter(
    prefix="/users/me",
    tags=["users"],
)


@router.get("/", response_model=UserRead)
async def get_me(token_data: dict = Depends(verify_token)):
    try:
        return await get_one_user(token_data.id, token_data.email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.patch("/update")
async def update_me(update_data: UserUpdate,token_data: UserRead = Depends(verify_token)):
    try:
        success = await update_user(token_data.id, update_data)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("/delete")
async def delete_me(token_data: UserRead = Depends(verify_token)):
    try:
        success = await delete_user(token_data.id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
@router.get("/languages", response_model=list[LanguageRead])
async def get_my_languages(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_languages(token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.get("/reports", response_model=list[ReportRead])
async def get_my_reports(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_reports(token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
