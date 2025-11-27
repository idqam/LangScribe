from fastapi import APIRouter, Depends, HTTPException, status
from Persistence.DTOs import (
    LanguageRead,
    ReportRead,
    UserCreate,
    UserLanguageCreate,
    UserLanguageRead,
    UserMessageCreate,
    UserMessageRead,
    UserRead,
    UserUpdate,
    UserLanguageUpdate
)
from Repositories import (
    delete_my_user_language,
    delete_user,
    get_languages,
    get_one_user,
    get_reports,
    post_message,
    post_user_language,
    update_user,
    patch_user_language,
    get_messages
)
from Resources import verify_token

router = APIRouter(
    prefix="/users/me",
    tags=["users"],
)


@router.get("/", response_model=UserRead)
async def get_me(token_data: UserRead = Depends(verify_token)):
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

################ LANGUAGES ###################################33

@router.get("/languages", response_model=list[UserLanguageRead])
async def get_my_languages(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_languages(token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/languages", response_model=UserLanguageRead)
async def post_my_languages(user_language: UserLanguageCreate,token_data: UserRead = Depends(verify_token)):
    try:
        return await post_user_language(user_lan_dto=user_language,id=token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.patch("/languages/{id}", response_model=UserLanguageRead)
async def patch_my_language(id: int,user_language: UserLanguageUpdate,token_data: UserRead = Depends(verify_token)):
    try:
        return await patch_user_language(token_data.id,id,user_language)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/languages/{id}", response_model=bool)
async def delete_my_language(id: int, token_data: UserRead = Depends(verify_token)):
    try:
        success = await delete_my_user_language(token_data.id,id)
        return bool(success)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

################### REPORT ###########################

@router.get("/reports", response_model=list[ReportRead])
async def get_my_reports(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_reports(token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

################## MESSAGES ##########################

@router.get("/messages", response_model=list[UserMessageRead])
async def get_my_messages(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_messages(token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/messages", response_model=UserMessageCreate)
async def post_add_message(message: UserMessageCreate, token_data: UserRead = Depends(verify_token)):
    try:
        return await post_message(token_data.id,message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
