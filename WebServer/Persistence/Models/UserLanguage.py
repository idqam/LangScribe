from datetime import datetime
from enum import StrEnum

from Persistence.Enums import PROFICIENCY_LEVELS
from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserLanguage(Base):
    __tablename__ = "user_languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete= "CASCADE"))
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id" ,ondelete="CASCADE"))
    proficiency_level: Mapped[PROFICIENCY_LEVELS] = mapped_column(SQLEnum(PROFICIENCY_LEVELS))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped["User"] = relationship(back_populates="user_languages")
    language: Mapped["Language"] = relationship(back_populates="user_languages", lazy='selectin' )

    __table_args__ = (
        UniqueConstraint("user_id", "language_id", name="uq_user_language"),
        Index("ix_user_id", "user_id"),
        Index("ix_language_id", "language_id"),
    )
