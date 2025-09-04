from pydantic import ConfigDict
from .schedule import ScheduleOutSchema
from .carevisit import CareVisitOutSchema
from .employee import EmployeeOutSchema
from .customer import CustomerOutSchema
from .measure import MeasureOutSchema
from typing import List


class ScheduleWithRelationsOutSchema(ScheduleOutSchema):
    employees: List[EmployeeOutSchema] = []
    customers: List[CustomerOutSchema] = []
    measures: List[MeasureOutSchema] = []
    care_visits: List[CareVisitOutSchema] = []
    model_config = ConfigDict(from_attributes=True)


class CareVisitWithRelationsOutSchema(CareVisitOutSchema):
    schedule: ScheduleOutSchema
    measures: List[MeasureOutSchema] = []
    employees: List[EmployeeOutSchema] = []
    model_config = ConfigDict(from_attributes=True)
