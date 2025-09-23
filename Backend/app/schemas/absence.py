from pydantic import BaseModel, ConfigDict
from datetime import date
from ..core.enums import AbsenceType


class AbsenceBaseSchema(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    absence_type: AbsenceType
    notes: str | None = None
    hours: int | None = None


class AbsenceUpdateSchema(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    absence_type: AbsenceType | None = None
    notes: str | None = None
    hours: int
    model_config = ConfigDict(extra="ignore")


class AbsenceOutSchema(AbsenceBaseSchema):
    id: int
    created: date
    model_config = ConfigDict(from_attributes=True)
