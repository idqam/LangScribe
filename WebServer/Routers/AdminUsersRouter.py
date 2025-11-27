from fastapi import APIRouter, Depends, HTTPException, status
from Persistence.DTOs import UserCreate, UserRead, UserUpdate
from Repositories import create_user, delete_user, get_all_users, get_one_user, update_user
from Resources import admin_required

#This is the router only admins should access to
#This is in onder to make users data more protected which only an user is going to get data
#by hitting the users router which should have prefix: users/me

router = APIRouter(
    prefix="/admin/users",
    tags=["users"],
)


@router.get("/", tags=["users"], response_model=list[UserRead])
async def read_users(token_data: UserRead = Depends(admin_required)) -> list[UserRead]:
    try:
        users: list[UserRead] = await get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", tags=["users"], response_model=UserRead)
async def read_user(id: int, token_data: UserRead = Depends(admin_required)) -> UserRead:
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
async def create_new_user(user_dto: UserCreate, token_data: UserRead = Depends(admin_required)) -> UserRead:
    try:
        user = await create_user(user_dto)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/{id}", tags=["users"], response_model=bool)
async def update_existing_user(id: int, user_dto: UserUpdate, token_data: UserRead = Depends(admin_required)):
    try:
        success = await update_user(id, user_dto)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{id}", tags=["users"], response_model=bool)
async def delete_existing_user(id: int, token_data: UserRead = Depends(admin_required)):

    try:
        success = await delete_user(id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

