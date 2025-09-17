from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime
from typing import Optional
from ..core.enums import ShiftType


class ScheduleBaseSchema(BaseModel):
    date: datetime
    shift_type: Optional[ShiftType] = None
    custom_shift: Optional[str] = None

    @model_validator(mode="after")
    def validate_shift(cls, values):
        if not values.shift_type and not values.custom_shift:
            raise ValueError("Either shift_type or custom_shift must be provided")
        if values.shift_type and values.custom_shift:
            raise ValueError("Only one of shift_type or custom_shift can be set")
        return values


class ScheduleUpdateSchema(BaseModel):
    date: Optional[datetime] = None
    shift_type: Optional[ShiftType] = None
    custom_shift: Optional[str] = None

    @model_validator(mode="after")
    def validate_shift(cls, values):
        if values.shift_type and values.custom_shift:
            raise ValueError("Only one of shift_type or custom_shift can be set")
        return values


class ScheduleOutSchema(BaseModel):
    id: int
    date: datetime
    shift_type: Optional[ShiftType] = None
    custom_shift: Optional[str] = None
    created: datetime

    model_config = ConfigDict(from_attributes=True)
