from fastapi import FastAPI
from resources import transaction
from sqlalchemy import text


from Persistence.DTOs import SubscriptionCreate, SubscriptionRead
from Persistence.Enums import SUBSCRIPTION_TIER
from Persistence.Models import Subscription

app = FastAPI(title="LangScribe API Gateway")


@app.get("/health")
async def health() -> dict[str, str]:
    async with transaction() as session:
        new_subscription = SubscriptionCreate(
            tier=SUBSCRIPTION_TIER.FREE,
            price=9.99,
            billing_period_months=1,
            features={
                "fuck-yes": "skibidi",
            },
            name="im fucking awesome"
        )
        subs = Subscription(**new_subscription.model_dump())
        session.add(subs)
        await session.flush()
        
    obj = SubscriptionRead.model_validate(subs)
    print(subs)
        
    return {"status": "fucking reat", "service": "{subs}"}
