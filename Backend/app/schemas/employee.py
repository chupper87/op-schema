from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from ..core.enums import Gender, RoleType
from typing import Optional


class EmployeeUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[RoleType] = None
    gender: Optional[Gender] = None
    birth_date: Optional[date] = None
    is_active: Optional[bool] = None

    employment_type: Optional[str] = None
    employment_degree: Optional[int] = None
    weekly_hours: Optional[int] = None
    vacation_days: Optional[int] = None
    is_summer_worker: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class EmployeeOutSchema(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str  # comes from user.email
    phone: Optional[str] = None
    role: Optional[RoleType] = None
    is_active: bool
    birth_date: Optional[date] = None
    created: datetime
    updated: datetime
    gender: Optional[Gender] = None

    employment_type: Optional[str] = None
    employment_degree: Optional[int] = None
    weekly_hours: Optional[int] = None
    vacation_days: Optional[int] = None
    is_summer_worker: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    user_id: int
    model_config = ConfigDict(from_attributes=True)


class EmployeeAdminCreateSchema(BaseModel):
    """Admin create full user if needed"""

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: Gender
    role: RoleType
    birth_date: date
    is_active: bool = True

    employment_type: Optional[str] = None
    employment_degree: Optional[int] = 100
    weekly_hours: Optional[int] = 40
    vacation_days: Optional[int] = 25
    is_summer_worker: Optional[bool] = False
    start_date: Optional[date] = None
    end_date: Optional[date] = None
