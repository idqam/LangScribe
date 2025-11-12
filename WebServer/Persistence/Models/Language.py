from enum import IntEnum

from sqlalchemy import DateTime, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from WebServer.Persistence.Models import Base


class CODE(IntEnum):
    ENGLISH = 0
    SPANISH = 1


class DIFICULTY(IntEnum):
    BEGINNER = 1
    ELEMENTARY = 2
    INTERMEDIATE = 3
    UPPER_INTERMEDIATE = 4
    ADVANCED = 5


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[CODE] = mapped_column(SQLEnum(CODE))
    name: Mapped[str] = mapped_column()
    dificulty: Mapped[DIFICULTY] = mapped_column(SQLEnum(DIFICULTY), default=DIFICULTY.INTERMEDIATE)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
