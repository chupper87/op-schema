from pydantic import BaseModel, ConfigDict
from datetime import datetime
from core.enums import ShiftType


class ScheduleBaseSchema(BaseModel):
    date: datetime
    shift: ShiftType


class ScheduleUpdateSchema(BaseModel):
    date: datetime | None = None
    shift: ShiftType | None = None


class ScheduleOutSchema(ScheduleBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)
