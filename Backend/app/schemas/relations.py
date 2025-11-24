from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..core.enums import TimeFlexibility, TimeOfDay
from typing import Optional, List


class CustomerMeasureBaseSchema(BaseModel):
    measure_id: int
    customer_id: int
    customer_duration: Optional[int] = None
    frequency: str  # t.ex. "daily", "weekly", "monthly"
    days_of_week: Optional[List[str]] = None  # t.ex. ["monday", "thursday"]
    occurrences_per_week: Optional[int] = None
    customer_notes: Optional[str] = None
    customer_time_of_day: Optional[TimeOfDay] = None
    customer_time_flexibility: Optional[TimeFlexibility] = None
    schedule_info: Optional[str] = None


class CustomerMeasureCreateSchema(BaseModel):
    measure_id: int
    customer_duration: Optional[int] = None
    frequency: str
    days_of_week: Optional[List[str]] = None
    occurrences_per_week: Optional[int] = None
    customer_notes: Optional[str] = None
    customer_time_of_day: Optional[TimeOfDay] = None
    customer_time_flexibility: Optional[TimeFlexibility] = None
    schedule_info: Optional[str] = None


class CustomerMeasureOutSchema(CustomerMeasureBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)


class CustomerMeasureWithMeasureSchema(CustomerMeasureOutSchema):
    measure_name: str
    measure_default_duration: int

    model_config = ConfigDict(from_attributes=True)


class ScheduleMeasureBaseSchema(BaseModel):
    schedule_id: int
    measure_id: int
    time_of_day: str | None = None
    custom_duration: int | None = None
    notes: str | None = None


class ScheduleMeasureOutSchema(ScheduleMeasureBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)


class ScheduleMeasureCreateSchema(BaseModel):
    measure_id: int
    time_of_day: str | None = None
    custom_duration: int | None = None
    notes: str | None = None


class ScheduleCustomerBaseSchema(BaseModel):
    schedule_id: int
    customer_id: int


class ScheduleCustomerOutSchema(ScheduleCustomerBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class ScheduleEmployeeBaseSchema(BaseModel):
    schedule_id: int
    employee_id: int


class ScheduleEmployeeOutSchema(ScheduleEmployeeBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class MeasureCareVisitBaseSchema(BaseModel):
    measure_id: int
    care_visit_id: int


class MeasureCareVisitOutSchema(MeasureCareVisitBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class EmployeeCareVisitBaseSchema(BaseModel):
    employee_id: int
    care_visit_id: int
    is_primary: bool = False
    notes: str | None = None


class EmployeeCareVisitOutSchema(EmployeeCareVisitBaseSchema):
    created: datetime
    model_config = ConfigDict(from_attributes=True)
