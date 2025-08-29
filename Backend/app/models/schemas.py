from pydantic import BaseModel, Field, EmailStr, ConfigDict
from enum import Enum
from datetime import datetime


# Enum
class RoleType(str, Enum):
    EMPLOYEE = "employee"
    ADMIN = "admin"
    ASSISTANT_NURSE = "assistant_nurse"
    CARE_ASSISTANT = "care_assistant"
    USER = "user"


class CareLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ShiftType(str, Enum):
    MORNING = "morning"
    DAY = "day"
    EVENING = "evening"
    NIGHT = "night"


class AbsenceType(str, Enum):
    SICK = "sick"
    VAB = "vab"
    VACATION = "vacation"
    PARENTAL_LEAVE = "parental_leave"
    LEAVE_OF_ABSCENCE = "leave_of_absence"


class VisitStatus(str, Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    CANCELED = "canceled"
    NO_SHOW = "no_show"
    PARTIALLY_COMPLETED = "partially_completed"
    RESCHEDULED = "rescheduled"


class TimeOfDay(str, Enum):
    MORNING = "morning"
    DAY = "day"
    EVENING = "evening"
    NIGHT = "night"


class TimeFlexibility(str, Enum):
    STRICT = "strict"
    STANDARD = "standard"
    FLEXIBLE = "flexible"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNSPECIFIED = "unspecified"


# =====================================


# Token
class TokenSchema(BaseModel):
    access_token: str
    token_type: str


# =====================================


# User schemas
class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    phone: str = Field(..., min_length=5, max_length=15)
    gender: Gender
    role: RoleType
    model_config = ConfigDict(from_attributes=True)


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superuser: bool
    is_active: bool
    created: datetime
    updated: datetime
    gender: Gender
    role: RoleType
    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    username: str
    password: str


# Employee schemas
class EmployeeBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: Gender
    role: RoleType
    birth_date: str
    is_active: bool = True

    # info
    employment_type: str
    employment_degree: int | None = 100
    weekly_hours: int | None = 40
    vacation_days: int | None = 25
    is_summer_worker: bool | None = False
    start_date: datetime
    end_date: datetime
