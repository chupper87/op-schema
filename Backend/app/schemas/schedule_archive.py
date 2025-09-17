from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from ..core.enums import ShiftType


class ScheduleArchiveBaseSchema(BaseModel):
    original_schedule_id: int
    original_date: date
    shift_type: ShiftType | None = None
    custom_shift: str | None = None
    notes: str | None = None


class ScheduleArchiveCreateSchema(ScheduleArchiveBaseSchema):
    original_created: datetime
    employee_count: int = 0
    customer_count: int = 0
    measure_count: int = 0
    visit_count: int = 0
    completed_visit_count: int = 0
    canceled_visit_count: int = 0
    employees_data: str | None = None
    customers_data: str | None = None
    measures_data: str | None = None
    visits_data: str | None = None


class ScheduleArchiveOutSchema(ScheduleArchiveBaseSchema):
    id: int
    archived_at: datetime
    original_created: datetime
    employee_count: int
    customer_count: int
    measure_count: int
    visit_count: int
    completed_visit_count: int
    canceled_visit_count: int
    employees_data: str | None = None
    customers_data: str | None = None
    measures_data: str | None = None
    visits_data: str | None = None
    model_config = ConfigDict(from_attributes=True)
