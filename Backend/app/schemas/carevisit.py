from pydantic import BaseModel, ConfigDict
from datetime import datetime
from core.enums import VisitStatus


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
