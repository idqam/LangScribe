from datetime import datetime
from enum import IntEnum

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from WebServer.Persistence.Models import Base


class Role(IntEnum):
    USER = 0
    ADMIN = 1
    # INSTITUION=2


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(hash=True)
    role: Mapped[Role] = mapped_column(SQLEnum(Role), default=Role.USER)
    pfp: Mapped[str | None] = mapped_column()
    day_streak: Mapped[int] = mapped_column(default=0)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"))
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    subscription: Mapped["Subscription"] = relationship()
