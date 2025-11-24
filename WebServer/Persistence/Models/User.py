from datetime import datetime
from enum import IntEnum

from Persistence.Enums import USER_ROLE
from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    uuid: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[USER_ROLE] = mapped_column(SQLEnum(USER_ROLE), default=USER_ROLE.USER)
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
    user_languages: Mapped[list["UserLanguage"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="user",
        cascade= "all, delete-orphan",
        lazy="selectin",
    )
    messages :Mapped[list["UserMessage"]] = relationship(back_populates="user",lazy="selectin")

    __table_args__ = (
        Index("ix_email", "email"),
        UniqueConstraint("email", name="uq_email"),
    )
