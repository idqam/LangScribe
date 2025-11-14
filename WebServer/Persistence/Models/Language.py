from datetime import datetime
from enum import IntEnum

from sqlalchemy import DateTime, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from WebServer.Persistence.Models import Base


class CODE(IntEnum):
    ENGLISH = 0
    SPANISH = 1


class DIFFICULTY(IntEnum):
    BEGINNER = 1
    ELEMENTARY = 2
    INTERMEDIATE = 3
    UPPER_INTERMEDIATE = 4
    ADVANCED = 5


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[CODE] = mapped_column(SQLEnum(CODE), unique=True)
    name: Mapped[str] = mapped_column()
    difficulty: Mapped[DIFFICULTY] = mapped_column(
        SQLEnum(DIFFICULTY),
        default=DIFFICULTY.INTERMEDIATE,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user_languages: Mapped[list["UserLanguage"]] = relationship(back_populates="language") # type: ignore
    prompts: Mapped[list["Prompt"]] = relationship(back_populates="language") # type: ignore
    reports: Mapped[list["Report"]] = relationship(back_populates="language") # type: ignore
