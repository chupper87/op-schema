from ..core.base import Base
from ..core.enums import VisitStatus
from sqlalchemy import ForeignKey, DateTime, Date, String, Integer, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date as date_type
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .schedule import Schedule
    from .measure import MeasureCareVisit
    from .employee import EmployeeCareVisit
    from .customer import Customer


class CareVisit(Base):
    __tablename__ = "care_visits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)

    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("ix_care_visit_date", "date"),
        Index("ix_care_visit_status", "status"),
        Index("ix_care_visit_customer_id", "customer_id"),
        Index("ix_care_visit_schedule_id", "schedule_id"),
        # Composite indexes for common query combinations
        Index("ix_care_visit_customer_date", "customer_id", "date"),
        Index("ix_care_visit_status_date", "status", "date"),
        Index("ix_care_visit_schedule_date", "schedule_id", "date"),
    )

    # Relationships
    schedule: Mapped["Schedule"] = relationship(
        "Schedule", back_populates="care_visits"
    )
    customer: Mapped["Customer"] = relationship(back_populates="care_visits")
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
