from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from WebServer.Persistence.Models import LENGUAGE_DIFFICULTY, Base


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    content: Mapped[dict] = mapped_column(JSON)
    difficulty: Mapped[LENGUAGE_DIFFICULTY] = mapped_column(
        SQLEnum(LENGUAGE_DIFFICULTY),
        default=LENGUAGE_DIFFICULTY.INTERMEDIATE,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    language: Mapped["Language"] = relationship(back_populates="prompts")
    messages: Mapped[list["UserMessage"]] = relationship(back_populates="prompt")
