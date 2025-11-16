from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from AIWorker.promptGen.promptEnums import PromptCategory
from WebServer.Persistence.Models import (
    LENGUAGE_DIFFICULTY,
    Base,
)


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    level: Mapped[str] = mapped_column(String(10))
    category: Mapped[PromptCategory] = mapped_column(SQLEnum(PromptCategory))
    difficulty: Mapped[LENGUAGE_DIFFICULTY] = mapped_column(
        SQLEnum(LENGUAGE_DIFFICULTY),
        default=LENGUAGE_DIFFICULTY.INTERMEDIATE,
    )
    content: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    language: Mapped["Language"] = relationship(back_populates="prompts")
    messages: Mapped[list["UserMessage"]] = relationship(back_populates="prompt")
