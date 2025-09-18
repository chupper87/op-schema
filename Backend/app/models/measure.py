from ..core.base import Base

from sqlalchemy import ForeignKey, DateTime, String, Integer, func, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .schedule import ScheduleMeasure
    from .customer import CustomerMeasure
    from .care_visit import CareVisit


class Measure(Base):
    __tablename__ = "measures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    default_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    time_of_day: Mapped[str] = mapped_column(String(20), nullable=True)
    time_flexibility: Mapped[str] = mapped_column(String(20), nullable=True)

    is_standard: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # Relationships
    care_visits: Mapped[List["MeasureCareVisit"]] = relationship(
        back_populates="measure"
    )
    schedules: Mapped[List["ScheduleMeasure"]] = relationship(back_populates="measure")
    customers: Mapped[List["CustomerMeasure"]] = relationship(back_populates="measure")

    def __repr__(self) -> str:
        return f"<Measure {self.name}>"


class MeasureCareVisit(Base):
    __tablename__ = "measure_care_visit"

    measure_id: Mapped[int] = mapped_column(ForeignKey("measures.id"), primary_key=True)
    care_visit_id: Mapped[int] = mapped_column(
        ForeignKey("care_visits.id"), primary_key=True
    )

    measure: Mapped["Measure"] = relationship(back_populates="care_visits")
    care_visit: Mapped["CareVisit"] = relationship(back_populates="measures")

    def __repr__(self) -> str:
        return f"<MeasureCareVisit {self.measure.name} {self.care_visit.date}>"
