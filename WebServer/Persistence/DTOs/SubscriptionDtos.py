from datetime import datetime
from decimal import Decimal
from typing import Any

from Persistence.Enums import SUBSCRIPTION_TIER
from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    tier: SUBSCRIPTION_TIER
    name: str
    price: Decimal
    billing_period_months: int
    features: dict[str, Any]


class SubscriptionRead(BaseModel):
    id: int
    tier: SUBSCRIPTION_TIER
    name: str
    price: Decimal
    billing_period_months: int
    features: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
