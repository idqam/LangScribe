from datetime import UTC, datetime, timedelta

from sqlalchemy import DateTime, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from WebServer.Persistence.Models import Base


class Tokens(Base):
    __tablename__ = "tokens"

    jti: Mapped[int] = mapped_column(primary_key=True)
    renewd_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC) + timedelta(hours=3),
    )

    __table_args__ = Index("ix_user", "user_id")
