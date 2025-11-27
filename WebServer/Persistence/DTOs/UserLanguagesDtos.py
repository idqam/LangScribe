from datetime import datetime

from Persistence.Enums import PROFICIENCY_LEVELS
from pydantic import BaseModel, ConfigDict


class UserLanguageCreate(BaseModel):
    user_id: int
    language_id: int
    proficiency_level: PROFICIENCY_LEVELS
    desired_level: PROFICIENCY_LEVELS


class UserLanguageUpdate(BaseModel):
    user_id: int
    proficiency_level: PROFICIENCY_LEVELS | None 
    desired_level: PROFICIENCY_LEVELS | None


class UserLanguageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    user_id: int
    language_id: int
    proficiency_level: PROFICIENCY_LEVELS
    desired_level: PROFICIENCY_LEVELS
    created_at: datetime
    updated_at: datetime


class UserLanguageDelete(BaseModel):
    id: int
