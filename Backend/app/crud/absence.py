from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..models.absence import Absence
from ..models.employee import Employee
from ..schemas.absence import AbsenceBaseSchema, AbsenceUpdateSchema
from ..core.exceptions import EmployeeNotFoundError
from ..core.enums import AbsenceType


def create_absence(db: Session, data: AbsenceBaseSchema) -> Absence:
    # Validate dates
    if data.start_date > data.end_date:
        raise ValueError("Start date cannot be after end date")

    # Verify employee exists
    stmt = select(Employee).where(Employee.id == data.employee_id)
    employee = db.execute(stmt).scalar_one_or_none()
    if not employee:
        raise EmployeeNotFoundError(data.employee_id)

    # Check for overlapping absences
    overlapping_stmt = select(Absence).where(
        Absence.employee_id == data.employee_id,
        Absence.start_date <= data.end_date,
        Absence.end_date >= data.start_date,
    )
    existing_absences = db.execute(overlapping_stmt).scalars().all()

    if existing_absences:
        raise ValueError(
            f"Absence overlaps with existing absence period from {existing_absences[0].start_date} to {existing_absences[0].end_date}"
        )

    try:
        absence = Absence(
            employee_id=data.employee_id,
            start_date=data.start_date,
            end_date=data.end_date,
            absence_type=data.absence_type,
            notes=data.notes,
            hours=data.hours,
        )
        db.add(absence)
        db.commit()
        db.refresh(absence)
        return absence
    except IntegrityError:
        db.rollback()
        raise


def get_absences(
    db: Session,
    employee_id: Optional[int] = None,
    absence_type: Optional[AbsenceType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    active_only: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Absence]:
    query = select(Absence).order_by(Absence.start_date)

    if employee_id is not None:
        query = query.where(Absence.employee_id == employee_id)

    if absence_type is not None:
        query = query.where(Absence.absence_type == absence_type)

    if start_date is not None:
        query = query.where(Absence.end_date >= start_date)

    if end_date is not None:
        query = query.where(Absence.start_date <= end_date)

    if active_only:
        from datetime import datetime

        today = datetime.now().date()
        query = query.where((Absence.start_date <= today) & (Absence.end_date >= today))

    query = query.offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())


def get_absence_by_id(db: Session, absence_id: int) -> Optional[Absence]:
    stmt = select(Absence).where(Absence.id == absence_id)

    absence = db.execute(stmt).scalar_one_or_none()

    return absence


def delete_absence(db: Session, absence_id: int) -> bool:
    stmt = select(Absence).where(Absence.id == absence_id)
    absence = db.execute(stmt).scalar_one_or_none()

    if not absence:
        return False

    try:
        db.delete(absence)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise


def update_absence(
    db: Session, absence_id: int, data: AbsenceUpdateSchema
) -> Optional[Absence]:
    stmt = select(Absence).where(Absence.id == absence_id)
    absence = db.execute(stmt).scalar_one_or_none()
    if not absence:
        return None

    final_start_date = (
        data.start_date if data.start_date is not None else absence.start_date
    )
    final_end_date = data.end_date if data.end_date is not None else absence.end_date

    if final_start_date > final_end_date:
        raise ValueError("Start date cannot be after end date")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(absence, field, value)

    try:
        db.commit()
        db.refresh(absence)
        return absence
    except IntegrityError:
        db.rollback()
        raise
