from datetime import datetime
from enum import IntEnum

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, func
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
    email: Mapped[str] = mapped_column(String(255))
    uuid: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()  # Remove hash=True, hash before storing
    role: Mapped[Role] = mapped_column(SQLEnum(Role), default=Role.USER)
    pfp: Mapped[str | None] = mapped_column()
    day_streak: Mapped[int] = mapped_column(server_default="0")
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"))
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    subscription: Mapped["Subscription"] = relationship(back_populates="users")
    user_languages: Mapped[list["UserLanguage"]] = relationship(back_populates="user")
    reports: Mapped[list["Report"]] = relationship(back_populates="user")

    __table_args__ = (
        Index("ix_email", "email"),
        UniqueConstraint("email", name="uq_email"),
    )
