from ..core.base import Base
from ..core.enums import RoleType
from typing import List, Optional

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, String, Boolean, func, Enum, Integer, Date, ForeignKey

from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schedule import ScheduleEmployee
    from .care_visit import CareVisit
    from .absence import Absence
    from .auth import User


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(15), unique=True, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role: Mapped[Optional[str]] = mapped_column(Enum(RoleType), nullable=True)

    employment_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    employment_degree: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weekly_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    vacation_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_summer_worker: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True, default=False
    )
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="employee")

    schedules: Mapped[List["ScheduleEmployee"]] = relationship(
        back_populates="employee"
    )
    care_visits: Mapped[List["EmployeeCareVisit"]] = relationship(
        back_populates="employee"
    )
    absences: Mapped[List["Absence"]] = relationship(back_populates="employee")

    @property
    def email(self) -> str:
        """Email kommer från User-tabellen"""
        return self.user.email

    @property
    def role_enum(self) -> Optional[RoleType]:
        if self.role:
            return RoleType(self.role)
        return None

    @role_enum.setter
    def role_enum(self, value: RoleType):
        self.role = value.value

    def __repr__(self) -> str:
        name = (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.user.email
        )
        return f"<Employee {name}>"


class EmployeeCareVisit(Base):
    __tablename__ = "employee_care_visit"

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id"), primary_key=True
    )
    care_visit_id: Mapped[int] = mapped_column(
        ForeignKey("care_visits.id"), primary_key=True
    )

    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    employee: Mapped["Employee"] = relationship(back_populates="care_visits")
    care_visit: Mapped["CareVisit"] = relationship(back_populates="employees")

    def __repr__(self) -> str:
        return f"<EmployeeCareVisit {self.employee.first_name} {self.employee.last_name} - {self.care_visit.date}>"
