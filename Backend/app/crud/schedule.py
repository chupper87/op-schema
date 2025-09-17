from typing import Optional
from datetime import date as date_type
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from ..schemas.schedule import ScheduleBaseSchema
from ..models.schedule import Schedule
from ..core.enums import ShiftType


def create_schedule(db: Session, data: ScheduleBaseSchema) -> Schedule:
    stmt = select(Schedule).where(Schedule.date == data.date)
    existing_schedule = db.execute(stmt).scalar_one_or_none()

    if existing_schedule:
        raise ValueError(f"Schedule for date {data.date} already exists.")

    try:
        schedule = Schedule(
            date=data.date, shift_type=data.shift_type, custom_shift=data.custom_shift
        )
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule
    except IntegrityError:
        db.rollback()
        raise


def get_schedules(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    shift_type: Optional[ShiftType] = None,
    date: Optional[date_type] = None,
    start_date: Optional[date_type] = None,
    end_date: Optional[date_type] = None,
) -> list[Schedule]:
    query = select(Schedule).order_by(Schedule.date).offset(skip).limit(limit)

    filters = []
    if shift_type:
        filters.append(Schedule.shift_type == shift_type)
    if date:
        filters.append(Schedule.date == date)
    if start_date:
        filters.append(Schedule.date >= start_date)
    if end_date:
        filters.append(Schedule.date <= end_date)

    if filters:
        query = query.where(and_(*filters))

    return list(db.execute(query).scalars().all())


def get_schedule_by_id(db: Session, schedule_id: int) -> Optional[Schedule]:
    stmt = select(Schedule).where(Schedule.id == schedule_id)
    return db.execute(stmt).scalar_one_or_none()


def update_schedule(db: Session, schedule_id: int, data: dict) -> Optional[Schedule]:
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return None

    for field, value in data.items():
        setattr(schedule, field, value)

    try:
        db.commit()
        db.refresh(schedule)
        return schedule
    except IntegrityError:
        db.rollback()
        raise


def delete_schedule(db: Session, schedule_id: int) -> bool:
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return False

    db.delete(schedule)
    db.commit()
    return True


def duplicate_schedule(
    db: Session, source_date: date_type, target_date: date_type
) -> Optional[Schedule]:
    stmt = select(Schedule).where(Schedule.date == source_date)
    source_schedule = db.execute(stmt).scalar_one_or_none()

    if not source_schedule:
        return None

    stmt = select(Schedule).where(Schedule.date == target_date)
    if db.execute(stmt).scalar_one_or_none():
        raise ValueError(f"Schedule for {target_date} already exists.")

    try:
        new_schedule = Schedule(
            date=target_date,
            shift_type=source_schedule.shift_type,
            custom_shift=source_schedule.custom_shift,
        )
        db.add(new_schedule)
        db.commit()
        db.refresh(new_schedule)
        return new_schedule
    except IntegrityError:
        db.rollback()
        raise
