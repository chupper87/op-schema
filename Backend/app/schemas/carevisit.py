from pydantic import BaseModel, ConfigDict
from datetime import datetime, date as date_type
from typing import List, Optional

from ..core.enums import VisitStatus
from .customer import CustomerOutSchema
from .measure import MeasureOutSchema
from .employee import EmployeeOutSchema
from .schedule import ScheduleOutSchema


class CareVisitBaseSchema(BaseModel):
    date: date_type
    status: VisitStatus
    duration: int
    notes: Optional[str] = None
    schedule_id: int
    customer_id: int


class CareVisitCreateSchema(CareVisitBaseSchema):
    pass


class CareVisitUpdateSchema(BaseModel):
    date: Optional[date_type] = None
    status: Optional[VisitStatus] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    schedule_id: Optional[int] = None
    customer_id: Optional[int] = None


class CareVisitOutSchema(CareVisitBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)


class CareVisitWithRelationsOutSchema(CareVisitOutSchema):
    schedule: ScheduleOutSchema
    customer: CustomerOutSchema
    measures: List[MeasureOutSchema] = []
    employees: List[EmployeeOutSchema] = []
    model_config = ConfigDict(from_attributes=True)
