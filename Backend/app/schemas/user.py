from pydantic import BaseModel, Field, EmailStr, ConfigDict
from ..core.enums import Gender, RoleType
from datetime import datetime, date
from typing import Optional


class UserInviteSchema(BaseModel):
    email: EmailStr
    is_superuser: bool = False


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=5, max_length=15)
    gender: Gender
    role: RoleType
    birth_date: date
    model_config = ConfigDict(from_attributes=True)


class UserCompleteRegistrationSchema(BaseModel):
    registration_token: str
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=5, max_length=15)
    gender: Gender
    role: RoleType
    birth_date: date


class UserOutSchema(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str] = None
    is_superuser: bool
    is_active: bool
    registration_completed: bool
    created: datetime
    updated: datetime
    model_config = ConfigDict(from_attributes=True)


class UserWithEmployeeOutSchema(UserOutSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[Gender] = None
    role: Optional[RoleType] = None
    birth_date: Optional[date] = None

    @classmethod
    def from_user(cls, user):
        """Create from User with Employee data"""
        data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "registration_completed": user.registration_completed,
            "created": user.created,
            "updated": user.updated,
        }

        if user.employee:
            data.update(
                {
                    "first_name": user.employee.first_name,
                    "last_name": user.employee.last_name,
                    "phone": user.employee.phone,
                    "gender": user.employee.gender,
                    "role": user.employee.role,
                    "birth_date": user.employee.birth_date,
                }
            )

        return cls(**data)


class UserLoginSchema(BaseModel):
    username: str
    password: str


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)


class RequestPasswordResetSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class ChangeRoleSchema(BaseModel):
    is_superuser: Optional[bool] = None
    role: Optional[RoleType] = None
