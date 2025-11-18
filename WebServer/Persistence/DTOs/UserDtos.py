from datetime import datetime

from Persistence.Enums import USER_ROLE
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    uuid: str
    email: str
    hashed_password: str
    pfp: str | None = None
    role: USER_ROLE | None = None


class UserUpdate(BaseModel):
    hashed_password: str | None = None
    pfp: str | None = None
    subscription_id: int | None = None
    role: USER_ROLE | None = None
    last_login: datetime | None = None


class UserRead(BaseModel):
    id: int
    uuid: str
    email: str
    role: USER_ROLE
    pfp: str | None = None
    subscription_id: int
    day_streak: int

    model_config = ConfigDict(from_attributes=True, extra="allow")


class UserDelete(BaseModel):
    id: int
