from pydantic import BaseModel, Field, EmailStr, ConfigDict
from ..core.enums import (
    Gender,
    RoleType,
)
from datetime import datetime, date


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    phone: str = Field(..., min_length=5, max_length=15)
    gender: Gender
    role: RoleType
    birth_date: date
    model_config = ConfigDict(from_attributes=True)


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superuser: bool
    created: datetime
    updated: datetime
    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    username: str
    password: str
