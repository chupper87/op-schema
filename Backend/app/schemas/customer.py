from pydantic import BaseModel, ConfigDict
from datetime import datetime
from core.enums import CareLevel, Gender


class CustomerBaseSchema(BaseModel):
    first_name: str
    last_name: str
    key_number: str
    address: str
    care_level: CareLevel
    gender: Gender
    approved_hours: float
    is_active: bool


class CustomerCreateSchema(CustomerBaseSchema):
    pass


class CustomerUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    key_number: str | None = None
    address: str | None = None
    care_level: str | None = None
    gender: Gender
    approved_hours: float | None = None
    is_active: bool | None = None


class CustomerOutSchema(CustomerBaseSchema):
    id: int
    created: datetime
    updated: datetime
    model_config = ConfigDict(from_attributes=True)
