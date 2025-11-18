from fastapi import APIRouter

router = APIRouter(
    prefix="/user_languages",
    tags=["user_languages"],
)


@router.get("/user_languages/", tags=["user_languages"])
async def read_user_languages():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/user_languages/", tags=["user_languages"])
async def create_user():
    return {"username": "fakecurrentuser"}


@router.put("/user_languages/{username}", tags=["user_languages"])
async def update_user(username: str):
    return {"username": username}


@router.delete("/user_languages/{username}", tags=["user_languages"])
async def delete_user(username: str):
    return {"username": username}
