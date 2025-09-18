from ..core.base import Base
from ..core.enums import CareLevel
from sqlalchemy import (
    ForeignKey,
    DateTime,
    Boolean,
    String,
    Integer,
    func,
    Float,
    Text,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .schedule import ScheduleCustomer
    from .measure import Measure
    from .care_visit import CareVisit


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    key_number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    care_level: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    approved_hours: Mapped[float | None] = mapped_column(
        Float, nullable=True, default=None
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # Relationships
    schedules: Mapped[List["ScheduleCustomer"]] = relationship(
        back_populates="customer"
    )
    care_visits: Mapped[List["CareVisit"]] = relationship(back_populates="customer")
    measures: Mapped[List["CustomerMeasure"]] = relationship(back_populates="customer")

    @property
    def care_level_enum(self) -> CareLevel:
        return CareLevel(self.care_level)

    def __repr__(self) -> str:
        return f"<Customer {self.first_name} {self.last_name}>"


class CustomerMeasure(Base):
    __tablename__ = "customer_measures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"), nullable=False
    )
    measure_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("measures.id"), nullable=False
    )

    customer_duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    customer_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    frequency: Mapped[str] = mapped_column(String(50), nullable=False, default="WEEKLY")
    days_of_week: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    occurrences_per_week: Mapped[int | None] = mapped_column(Integer, nullable=True)

    customer_time_of_day: Mapped[str | None] = mapped_column(String(20), nullable=True)
    customer_time_flexibility: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )
    schedule_info: Mapped[str | None] = mapped_column(Text, nullable=True)

    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="measures")
    measure: Mapped["Measure"] = relationship("Measure", back_populates="customers")

    def __repr__(self) -> str:
        return f"<CustomerMeasure customer_id={self.customer_id} measure_id={self.measure_id}>"
