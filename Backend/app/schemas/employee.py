from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from core.enums import Gender, RoleType


class EmployeeBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
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
