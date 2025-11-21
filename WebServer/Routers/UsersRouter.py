from fastapi import APIRouter, HTTPException, status
from Persistence.DTOs import UserCreate, UserRead, UserUpdate
from Repositories import create_user, delete_user, get_all_users, get_one_user, update_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", tags=["users"], response_model=list[UserRead])
async def read_users() -> [UserRead]:
    try:
        users = await get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", tags=["users"], response_model=UserRead)
async def read_user(id: int) -> UserRead:
    try:
        user = await get_one_user(id, email= None)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/",
    tags=["users"],
    response_model=UserRead,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(user_dto: UserCreate) -> UserRead:
    try:
        user = await create_user(user_dto)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/{id}", tags=["users"], response_model=bool)
async def update_existing_user(id: int, user_dto: UserUpdate):
    try:
        success = await update_user(id, user_dto)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{id}", tags=["users"], response_model=bool)
async def delete_existing_user(id: int):

    try:
        success = await delete_user(id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
