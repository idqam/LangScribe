from fastapi import APIRouter

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get("/reports/", tags=["reports"])
async def read_report():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/reports/me", tags=["reports"])
async def create_report():
    return {"username": "fakecurrentuser"}


@router.put("/reports/{username}", tags=["reports"])
async def update_report(username: str):
    return {"username": username}


@router.delete("/reports/{username}", tags=["reports"])
async def delete_report(username: str):
    return {"username": username}
