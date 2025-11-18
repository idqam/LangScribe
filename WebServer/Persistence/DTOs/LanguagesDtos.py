from datetime import datetime

from Persistence.Enums import LANGUAGE_CODE, LANGUAGE_DIFFICULTY
from pydantic import BaseModel, ConfigDict


class LanguageCreate(BaseModel):
    code: str
    name: str
    difficulty: LANGUAGE_DIFFICULTY | None = None



class LanguageUpdate(BaseModel):
    name: str | None = None
    difficulty: LANGUAGE_DIFFICULTY | None = None


class LanguageRead(BaseModel):

    id: int
    code: LANGUAGE_CODE
    name: str
    difficulty: LANGUAGE_DIFFICULTY
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True, extra="allow")

class LanguageDelete(BaseModel):
    id: int
