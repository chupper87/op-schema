from ..core.base import Base
from ..core.enums import ShiftType

from sqlalchemy import ForeignKey, DateTime, String, Integer, func, Text, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date as date_type
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .schedule import ScheduleMeasure
    from .employee import Employee
    from .care_visit import CareVisit
    from .measure import Measure
    from .customer import Customer


class Schedule(Base):
    __tablename__ = "schedules"

    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    shift_type: Mapped[ShiftType | None] = mapped_column(Enum(ShiftType), nullable=True)
    custom_shift: Mapped[str | None] = mapped_column(String(50), nullable=True)

    employees: Mapped[List["ScheduleEmployee"]] = relationship(
        back_populates="schedule"
    )
    measures: Mapped[List["ScheduleMeasure"]] = relationship(back_populates="schedule")
    customers: Mapped[List["ScheduleCustomer"]] = relationship(
        back_populates="schedule"
    )
    care_visits: Mapped[List["CareVisit"]] = relationship(back_populates="schedule")

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<Schedule {self.date}>"


class ScheduleArchive(Base):
    __tablename__ = "schedule_archives"

    original_schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_date: Mapped[date_type] = mapped_column(Date, nullable=False)

    shift_type: Mapped[ShiftType | None] = mapped_column(Enum(ShiftType), nullable=True)
    custom_shift: Mapped[str | None] = mapped_column(String(50), nullable=True)

    employee_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    customer_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    measure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    visit_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed_visit_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    canceled_visit_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    employees_data: Mapped[str] = mapped_column(Text, nullable=True)
    customers_data: Mapped[str] = mapped_column(Text, nullable=True)
    measures_data: Mapped[str] = mapped_column(Text, nullable=True)
    visits_data: Mapped[str] = mapped_column(Text, nullable=True)

    archived_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    original_created: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        shift_info = self.shift_type.value if self.shift_type else self.custom_shift
        return f"<ScheduleArchive {self.original_date} (original_id={self.original_schedule_id}, shift={shift_info})>"


class ScheduleEmployee(Base):
    __tablename__ = "schedule_employee"

    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id"), primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id"), primary_key=True
    )

    schedule: Mapped["Schedule"] = relationship(back_populates="employees")
    employee: Mapped["Employee"] = relationship(back_populates="schedules")


class ScheduleMeasure(Base):
    __tablename__ = "schedule_measure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"), nullable=False)
    measure_id: Mapped[int] = mapped_column(ForeignKey("measures.id"), nullable=False)

    time_of_day: Mapped[str] = mapped_column(String(20), nullable=True)
    custom_duration: Mapped[int] = mapped_column(Integer, nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    schedule: Mapped["Schedule"] = relationship(back_populates="measures")
    measure: Mapped["Measure"] = relationship(back_populates="schedules")

    def __repr__(self) -> str:
        time_info = f" ({self.time_of_day})" if self.time_of_day else ""
        return f"<ScheduleMeasure {self.measure.name}{time_info}>"


class ScheduleCustomer(Base):
    __tablename__ = "schedule_customer"

    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id"), primary_key=True
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), primary_key=True
    )

    schedule: Mapped["Schedule"] = relationship(back_populates="customers")
    customer: Mapped["Customer"] = relationship(back_populates="schedules")
