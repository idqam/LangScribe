from fastapi import APIRouter, Depends, HTTPException, status
from Persistence.DTOs import (
    UserLanguageCreate,
    UserLanguageRead,
)
from Repositories import create_user_languages, delete_user_languages, get_all_user_languages
from Resources import admin_required, verify_token

router = APIRouter(
    prefix="/user_languages",
    tags=["user_languages"],
)


@router.get("/", tags=["user_languages"], response_model=list[UserLanguageRead])
async def read_user_languages(token_data: dict = Depends(admin_required)) -> [UserLanguageRead]:
    try:
        user_languages = await get_all_user_languages()
        return user_languages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/",
    tags=["user_languages"],
    response_model=UserLanguageRead,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user_language(user_language_dto: UserLanguageCreate, token_data: dict = Depends(admin_required)) -> UserLanguageRead:
    try:
        user_language = await create_user_languages(user_language_dto)
        return user_language
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("/{id}", tags=["user_languages"], response_model=bool)
async def delete_existing_user_language(id: int, token_data: dict = Depends(admin_required)):
    try:
        success = await delete_user_languages(id, token_data.id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
