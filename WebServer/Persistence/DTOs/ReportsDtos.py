from datetime import datetime
from typing import Any

from Persistence.Enums import RATE
from pydantic import BaseModel, ConfigDict


class ReportCreate(BaseModel):
    user_id: int
    language_id: int
    user_message_id: int
    content: dict[str, Any]
    rating: RATE


class ReportUpdate(BaseModel):
    content: dict[str, Any] | None = None
    rating: RATE | None = None


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    user_id: int
    language_id: int
    user_message_id: int
    content: dict[str, Any]
    rating: RATE
    created_at: datetime


class ReportDelete(BaseModel):
    id: int
