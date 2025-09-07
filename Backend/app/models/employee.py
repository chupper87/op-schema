from ..core.base import Base
from ..core.enums import RoleType
from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, String, Boolean, func, Enum, Integer, Date, ForeignKey

from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schedule import ScheduleEmployee
    from .employee import Employee
    from .care_visit import CareVisit
    from .absence import Absence


class Employee(Base):
    __tablename__ = "employee"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role: Mapped[str] = mapped_column(Enum(RoleType), nullable=False)

    employment_type: Mapped[str] = mapped_column(String(20), nullable=True)
    employment_degree: Mapped[int] = mapped_column(Integer, nullable=True)
    weekly_hours: Mapped[int] = mapped_column(Integer, nullable=True)
    vacation_days: Mapped[int] = mapped_column(Integer, nullable=True)
    is_summer_worker: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=False
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    schedules: Mapped[List["ScheduleEmployee"]] = relationship(
        back_populates="employee"
    )
    care_visits: Mapped[List["EmployeeCareVisit"]] = relationship(
        back_populates="employee"
    )
    absences: Mapped[List["Absence"]] = relationship(back_populates="employee")

    @property
    def role_enum(self) -> RoleType:
        return RoleType(self.role)

    @role_enum.setter
    def role_enum(self, value: RoleType):
        self.role = value.value

    def __repr__(self) -> str:
        return f"<Employee {self.first_name} {self.last_name}>"


class EmployeeCareVisit(Base):
    __tablename__ = "employee_care_visit"

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id"), primary_key=True
    )
    care_visit_id: Mapped[int] = mapped_column(
        ForeignKey("care_visits.id"), primary_key=True
    )

    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    employee: Mapped["Employee"] = relationship(back_populates="care_visits")
    care_visit: Mapped["CareVisit"] = relationship(back_populates="employees")

    def __repr__(self) -> str:
        return f"<EmployeeCareVisit {self.employee.first_name} {self.employee.last_name} - {self.care_visit.date}>"
