from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from WebServer.Persistence.Models import LENGUAGE_DIFICULTY, Base


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    content: Mapped[JSON] = mapped_column()
    difficulty: Mapped[LENGUAGE_DIFICULTY] = mapped_column(
        SQLEnum(LENGUAGE_DIFICULTY),
        default=LENGUAGE_DIFICULTY.INTERMEDIATE,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    language: Mapped["Language"] = relationship(back_populates="languages")
