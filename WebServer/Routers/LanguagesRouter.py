from fastapi import APIRouter, HTTPException, status
from Persistence.DTOs import LanguageCreate, LanguageDelete, LanguageRead, LanguageUpdate
from Repositories import create_language, delete_language, get_all_languages, get_one_language, update_language
from loguru import logger

router = APIRouter(
    prefix="/languages",
    tags=["languages"],
)


@router.get("/", tags=["languages"], response_model=list[LanguageRead])
async def read_languages() -> [LanguageRead]:
    try:
        languages = await get_all_languages()
        return languages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/{id}", tags=["languages"], response_model=LanguageRead)
async def read_language(id: int) -> LanguageRead:
    try:
        language = await get_one_language(id, email= None)
        return language
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/",
    tags=["languages"],
    response_model=LanguageRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_language(language_dto: LanguageCreate) -> LanguageRead:
    try:
        logger.error("router")
        language = await create_language(language_dto)
        return language
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/{id}", tags=["languages"], response_model=bool)
async def update_existing_language(id: int, language_dto: LanguageUpdate):
    try:
        success = await update_language(id, language_dto)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{id}", tags=["languages"], response_model=bool)
async def delete_existing_language(id: int):

    try:
        success = await delete_language(id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
