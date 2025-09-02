from ..core.base import Base
from ..core.enums import AbsenceType
from sqlalchemy import ForeignKey, DateTime, Date, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee


class Absence(Base):
    __tablename__ = "absences"

    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    absence_type: Mapped[str] = mapped_column(String(20), nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    hours: Mapped[int] = mapped_column(Integer, nullable=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    employee: Mapped["Employee"] = relationship(back_populates="absences")

    @property
    def absence_type_enum(self) -> AbsenceType:
        return AbsenceType(self.absence_type)

    @absence_type_enum.setter
    def absence_type_enum(self, value: AbsenceType):
        self.absence_type = value.value

    def __repr__(self) -> str:
        return f"<Absence {self.employee.first_name} {self.employee.last_name}: {self.absence_type} {self.start_date} - {self.end_date}>"
