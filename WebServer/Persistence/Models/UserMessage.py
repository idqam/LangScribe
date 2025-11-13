from sqlalchemy import JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from WebServer.Persistence.Models import Base


class UserMessage(Base):
    __tablename__ = "user_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    prompt_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    content: Mapped[JSON] = mapped_column(JSON)

    prompt: Mapped["Prompt"] = relationship(back_populates="messages")
    report: Mapped["Report"] = relationship(back_populates="message")
    __table_args__ = (Index("ix_user_id", "user_id"),)
