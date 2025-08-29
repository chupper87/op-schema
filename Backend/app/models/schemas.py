from pydantic import BaseModel, Field, EmailStr
from enum import Enum


# Enum
# =====================================


class RoleType(str, Enum):
    EMPLOYEE = "emplotyee"
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
    LEAVE_OF_ABSCENCE = "leave_of_abscence"


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


# =====================================


# Token
class TokenSchema(BaseModel):
    access_token: str
    token_type: str


# User schemas
class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
