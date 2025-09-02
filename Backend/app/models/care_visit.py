from ..core.base import Base
from ..core.enums import VisitStatus
from sqlalchemy import ForeignKey, DateTime, Date, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date as date_type
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .schedule import Schedule
    from .measure import MeasureCareVisit
    from .employee import EmployeeCareVisit


class CareVisit(Base):
    __tablename__ = "care_visits"

    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"), nullable=False)
    schedule: Mapped["Schedule"] = relationship(
        "Schedule", back_populates="care_visits"
    )
    measures: Mapped[List["MeasureCareVisit"]] = relationship(
        back_populates="care_visit"
    )
    employees: Mapped[List["EmployeeCareVisit"]] = relationship(
        back_populates="care_visit"
    )

    @property
    def status_enum(self) -> VisitStatus:
        return VisitStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: VisitStatus):
        self.status = value.value

    def __repr__(self) -> str:
        return f"<CareVisit {self.date}>"
