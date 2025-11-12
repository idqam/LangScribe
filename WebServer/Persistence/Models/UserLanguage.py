from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from WebServer.Persistence.Models import Base, Language, User


class PROFICIENCY_LEVELS(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class UserLanguage(Base):
    __tablename__ = "user_languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    proficiency_level: Mapped[PROFICIENCY_LEVELS] = mapped_column(
        String(2),
        SQLEnum(PROFICIENCY_LEVELS),
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped["User"] = relationship(back_populates="users")
    Language: Mapped["Language"] = relationship(back_populates="languages")

    __table_args__ = (
        UniqueConstraint("user_id", "language_id", name="uq_user_language"),
        Index("ix_user_id", "user_id"),
        Index("ix_language_id", "language_id"),
    )
