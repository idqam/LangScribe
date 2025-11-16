from typing import Any

from pydantic import BaseModel, ConfigDict


class UserMessageCreate(BaseModel):
    user_id: int
    prompt_id: int
    content: dict[str, Any]


class UserMessageUpdate(BaseModel):
    content: dict[str, Any] | None = None


class UserMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    prompt_id: int
    content: dict[str, Any]


class UserMessageDelete(BaseModel):
    id: int
