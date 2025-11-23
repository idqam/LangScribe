from fastapi import APIRouter, Depends, HTTPException, status
from Persistence.DTOs import (
    UserMessageCreate,
    UserMessageRead,
    UserTokenPayload,
)
from Repositories import create_usermessage, delete_usermessage, get_all_usermessages
from Resources import admin_required, verify_token

router = APIRouter(
    prefix="/usermessages",
    tags=["usermessages"],
)


@router.get("/", tags=["usermessages"], response_model=list[UserMessageRead])
async def read_usermessages(
    token_data: UserTokenPayload = Depends(admin_required),
) -> [UserMessageRead]:
    try:
        usermessages = await get_all_usermessages()
        return usermessages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/",
    tags=["usermessages"],
    response_model=UserMessageRead,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_201_CREATED,
)
async def create_new_usermessage(
    usermessage_dto: UserMessageCreate,
    token_data: UserTokenPayload = Depends(verify_token),
) -> UserMessageRead:
    try:
        usermessage = await create_usermessage(usermessage_dto)
        return usermessage
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{id}", tags=["usermessages"], response_model=bool)
async def delete_existing_usermessage(
    id: int,
    token_data: UserTokenPayload = Depends(admin_required),
):
    try:
        success = await delete_usermessage(id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
