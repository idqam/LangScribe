from datetime import UTC, datetime, timedelta

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Token(Base):
    __tablename__ = "tokens"

    jti: Mapped[int] = mapped_column(primary_key=True)
    renewd_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC) + timedelta(hours=3),
    )
