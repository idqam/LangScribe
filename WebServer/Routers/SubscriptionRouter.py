from fastapi import APIRouter, HTTPException, status
from Persistence.DTOs import SubscriptionCreate, SubscriptionRead
from Repositories import create_subscription, delete_subscription, get_all_subscriptions

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


@router.get("/", tags=["subscriptions"], response_model=list[SubscriptionRead])
async def read_subscriptions() -> [SubscriptionRead]:
    try:
        subscriptions = await get_all_subscriptions()
        return subscriptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/",
    tags=["subscriptions"],
    response_model=SubscriptionRead,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_201_CREATED,
)
async def create_new_subscription(subscription_dto: SubscriptionCreate) -> SubscriptionRead:
    try:
        subscription = await create_subscription(subscription_dto)
        return subscription
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("/{id}", tags=["subscriptions"], response_model=bool)
async def delete_existing_subscription(id: int):

    try:
        success = await delete_subscription(id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
