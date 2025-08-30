from pydantic import BaseModel, ConfigDict
from datetime import datetime
from core.enums import TimeFlexibility, TimeOfDay


class MeasureBaseSchema(BaseModel):
    name: str
    default_duration: int
    text: str | None = None
    time_of_day: TimeOfDay | None = None
    time_flexibility: TimeFlexibility | None = TimeFlexibility.STANDARD


class MeasureUpdateSchema(BaseModel):
    name: str | None = None
    default_duration: int | None = None
    text: str | None = None
    time_of_day: TimeOfDay | None = None
    time_flexibility: TimeFlexibility | None = None


class MeasureOutSchema(MeasureBaseSchema):
    id: int
    created: datetime
    model_config = ConfigDict(from_attributes=True)
