from datetime import datetime
from typing import Any

from Persistence.Enums import LANGUAGE_DIFFICULTY
from sqlalchemy import JSON, DateTime, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id", ondelete="CASCADE"))
    content: Mapped[dict[str, Any]] = mapped_column(JSON)
    difficulty: Mapped[LANGUAGE_DIFFICULTY] = mapped_column(
        SQLEnum(LANGUAGE_DIFFICULTY),
        default=LANGUAGE_DIFFICULTY.INTERMEDIATE,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    language: Mapped["Language"] = relationship(back_populates="prompts")
    messages: Mapped[list["UserMessage"]] = relationship(back_populates="prompt")
