from datetime import datetime
from typing import Any

from Persistence.Enums import LANGUAGE_DIFFICULTY
from pydantic import BaseModel, ConfigDict


class PromptCreate(BaseModel):
    language_id: int
    content: dict[str, Any]
    difficulty: LANGUAGE_DIFFICULTY | None = None


class PromptUpdate(BaseModel):
    language_id: int | None = None
    content: dict[str, Any] | None = None
    difficulty: LANGUAGE_DIFFICULTY | None = None


class PromptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    language_id: int
    content: dict[str, Any]
    difficulty: LANGUAGE_DIFFICULTY
    created_at: datetime


class PromptDelete(BaseModel):
    id: int
