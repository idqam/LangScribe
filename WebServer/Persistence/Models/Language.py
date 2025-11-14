from datetime import datetime
from enum import IntEnum

from sqlalchemy import DateTime, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base

from ..Enums import LANGUAGE_CODE, LANGUAGE_DIFFICULTY


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[LANGUAGE_CODE] = mapped_column(SQLEnum(LANGUAGE_CODE), unique=True)
    name: Mapped[str] = mapped_column()
    difficulty: Mapped[LANGUAGE_DIFFICULTY] = mapped_column(
        SQLEnum(LANGUAGE_CODE),
        default=LANGUAGE_DIFFICULTY.INTERMEDIATE,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user_languages: Mapped[list["UserLanguage"]] = relationship(back_populates="language")
    prompts: Mapped[list["Prompt"]] = relationship(back_populates="language")
    reports: Mapped[list["Report"]] = relationship(back_populates="language")
