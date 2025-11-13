from datetime import datetime
from enum import IntEnum

from sqlalchemy import JSON, DateTime, ForeignKey, Index, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from WebServer.Persistence.Models import Base


class RATE(IntEnum):
    NOVICE = 1
    BEGINNER = 2
    COMPETENT = 3
    PROFICIENT = 4
    EXPERT = 5


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    user_message_id: Mapped[int] = mapped_column(ForeignKey("user_messages.id"))
    content: Mapped[JSON] = mapped_column(JSON)
    rating: Mapped[RATE] = mapped_column(SQLEnum(RATE))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="reports")
    message: Mapped["UserMessage"] = relationship(back_populates="report")
    language: Mapped["Language"] = relationship(back_populates="reports")

    __table_args__ = (
        Index("ix_user", "user_id"),
        Index("ix_message", "user_message_id"),
    )
