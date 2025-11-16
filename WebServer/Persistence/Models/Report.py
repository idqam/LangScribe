from datetime import datetime
from enum import IntEnum
from typing import Any

from Persistence.Enums import RATE
from sqlalchemy import JSON, DateTime, ForeignKey, Index, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    user_message_id: Mapped[int] = mapped_column(ForeignKey("user_messages.id"))
    content: Mapped[dict[str, Any]] = mapped_column(JSON)
    rating: Mapped[RATE] = mapped_column(SQLEnum(RATE))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="reports")
    message: Mapped["UserMessage"] = relationship(back_populates="report")
    language: Mapped["Language"] = relationship(back_populates="reports")

    __table_args__ = (
        Index("ix_user", "user_id"),
        Index("ix_message", "user_message_id"),
    )
