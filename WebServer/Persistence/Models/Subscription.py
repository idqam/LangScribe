from datetime import datetime
from decimal import Decimal
from enum import IntEnum
from typing import Any

from sqlalchemy import JSON, DateTime, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Models import Base

from ..Enums import SUBSCRIPTION_TIER


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    tier: Mapped[SUBSCRIPTION_TIER] = mapped_column(SQLEnum(SUBSCRIPTION_TIER), unique=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column()
    billing_period_months: Mapped[int] = mapped_column()
    features: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    users: Mapped[list["User"]] = relationship(back_populates="subscription")
