from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from ..Enums import SUBSCRIPTION_TIER


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
    upated_at: datetime
    model_config = {"from_attributes": True}