from datetime import datetime

from pydantic import BaseModel

from ..Enums import USER_ROLE


class UserCreate(BaseModel):
    email: str
    password: str
    pfp: str | None
    role: USER_ROLE | None


class UserUpdate(BaseModel):
    password: str | None
    pfp: str | None
    subscription_id: int | None
    role: USER_ROLE | None
    last_login: datetime | None


class UserRead(BaseModel):
    id: int
    uuid: str
    email: str
    role: USER_ROLE
    pfp: str | None
    subscription_id: int
    day_streak: int
    model_config = {"from_attributes": True}


class UserDelete(BaseModel):
    id: int
