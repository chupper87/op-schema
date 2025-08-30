from pydantic import BaseModel, ConfigDict
from datetime import datetime
from core.enums import TimeFlexibility, TimeOfDay


class CustomerMeasureBaseSchema(BaseModel):
    measure_id: int
    customer_id: int
    customer_duration: int | None = None
    customer_frequency: str | None = None
    customer_notes: str | None = None
    customer_time_of_day: TimeOfDay | None = None
    customer_time_flexibility: TimeFlexibility | None = None
    schedule_info: str | None = None


class CustomerMeasureCreateSchema(BaseModel):
    measure_id: int
    customer_duration: int | None = None
    customer_frequency: str | None = None
    customer_notes: str | None = None
    customer_time_of_day: TimeOfDay | None = None
    customer_time_flexibility: TimeFlexibility | None = None
    schedule_info: str | None = None


class CustomerMeasureOutSchema(CustomerMeasureBaseSchema):
    id: int
    created: datetime
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
