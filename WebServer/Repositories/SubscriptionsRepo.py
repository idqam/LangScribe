from Persistence.DTOs import SubscriptionCreate
from Persistence.Models import Subscription
from Resources import transaction
from sqlalchemy import delete, select


async def get_all_subscriptions() -> [Subscription]:
    async with transaction() as session:
        res = await session.execute(
            select(Subscription),
        )

        subscriptions = res.scalars().all()

    return subscriptions


async def create_subscription(tmp_subscription: SubscriptionCreate) -> Subscription:
    async with transaction() as session:

        new_subscription = Subscription(**tmp_subscription.model_dump())
        session.add(new_subscription)
        await session.flush()
        await session.refresh(new_subscription)

    return new_subscription


async def delete_subscription(id: int) -> bool:
    async with transaction() as session:
        subscription = await session.get(Subscription,id)

        if not subscription:
            raise ValueError("Subscription not found")

        res = await session.execute(
            delete(Subscription).where(Subscription.id == id),
        )

        if not res.rowcount:
            raise ValueError("No rows were affected")


    return res.rowcount
