from fastapi import APIRouter

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


@router.get("/subscriptions/", tags=["subscriptions"])
async def read_subscriptions():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/subscriptions/", tags=["subscriptions"])
async def create_subscriptions():
    return {"username": "fakecurrentuser"}
