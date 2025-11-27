from datetime import datetime, timezone

from Persistence.Enums import USER_ROLE
from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    uuid: str
    email: str
    hashed_password: str
    pfp: str | None = None
    role: USER_ROLE | None = None
    new_user: bool = True
    last_login: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    day_streak: int = 1

class UserUpdate(BaseModel):
    hashed_password: str | None = None
    pfp: str | None = None
    subscription_id: int | None = None
    role: USER_ROLE | None = None
    new_user: bool | None = None
    last_login: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

## This is what the jwt would look like once is decoded
class UserRead(BaseModel):
    id: int
    uuid: str
    email: str
    role: USER_ROLE
    pfp: str | None = None
    subscription_id: int
    day_streak: int
    new_user: bool
    model_config = ConfigDict(from_attributes=True, extra="allow")


class UserDelete(BaseModel):
    id: int
