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

    employment_type: str
    employment_degree: int | None = 100
    weekly_hours: int | None = 40
    vacation_days: int | None = 25
    is_summer_worker: bool | None = False
    start_date: datetime
    end_date: datetime


class EmployeeCreateSchema(EmployeeBaseSchema):
    pass


class EmployeeUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    role: RoleType | None = None
    gender: Gender
    birth_date: str | None = None
    is_active: bool | None = None

    employment_type: str | None = None
    employment_degree: int | None = None
    weekly_hours: int | None = None
    vacation_days: int | None = None
    is_summer_worker: bool | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class EmployeeOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: RoleType
    is_active: bool
    birth_date: str
    created: datetime
    updated: datetime
    gender: Gender

    employment_type: str | None = None
    employment_degree: int | None = None
    weekly_hours: int | None = None
    vacation_days: int | None = None
    is_summer_worker: bool | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


# Customer schemas
class CustomerBaseSchema(BaseModel):
    first_name: str
    last_name: str
    key_number: str
    address: str
    care_level: CareLevel
    gender: Gender
    approved_hours: float
    is_active: bool


class CustomerCreateSchema(CustomerBaseSchema):
    pass


class CustomerUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    key_number: str | None = None
    address: str | None = None
    care_level: str | None = None
    gender: Gender
    approved_hours: float | None = None
    is_active: bool | None = None


class CustomerOutSchema(CustomerBaseSchema):
    id: int
    created: datetime
    updated: datetime
    model_config = ConfigDict(from_attributes=True)


# Measure schemas
class MeasureBaseSchema(BaseModel):
    name: str
    default_duration: int
    text: str | None = None
    time_of_day: TimeOfDay | None = None
    time_flexibility: TimeFlexibility | None = TimeFlexibility.STANDARD


class MeasureCreateSchema(MeasureBaseSchema):
    pass


class MeasureUpdateSchema(BaseModel):
    name: str | None = None
    default_duration: int | None = None
    text: str | None = None
    time_of_day: TimeOfDay | None = None
    time_flexibility: TimeFlexibility | None = None


class MeasureOutSchema(MeasureBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)


# Schedule schemas
class ScheduleBaseSchema(BaseModel):
    date: datetime
    shift: ShiftType


class ScheduleCreateSchema(ScheduleBaseSchema):
    pass


class ScheduleUpdateSchema(BaseModel):
    date: datetime | None = None
    shift: ShiftType | None = None


class ScheduleOutSchema(ScheduleBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)


# CareVisit schemas
class CareVisitBaseSchema(BaseModel):
    date: datetime
    status: VisitStatus
    duration: int
    notes: str | None = None
    schedule_id: int


class CareVisitCreateSchema(CareVisitBaseSchema):
    pass


class CareVisitUpdateSchema(BaseModel):
    date: datetime | None = None
    status: VisitStatus | None = None
    duration: int | None = None
    notes: str | None = None
    schedule_id: int | None = None
    model_config = ConfigDict(exclude_none=True)


class CareVisitOutSchema(CareVisitBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)
