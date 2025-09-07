from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..core.enums import AbsenceType


class AbsenceBaseSchema(BaseModel):
    employee_id: int
    start_date: datetime
    end_date: datetime
    absence_type: AbsenceType
    notes: str
    hours: int


class AbsenceUpdateSchema(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    absence_type: AbsenceType | None = None
    notes: str | None = None
    hours: int
    model_config = ConfigDict(extra="ignore")


class AbsenceOutSchema(AbsenceBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)
