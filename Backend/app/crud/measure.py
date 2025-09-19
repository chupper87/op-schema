from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..schemas.measure import MeasureBaseSchema
from ..models.measure import Measure
from ..core.enums import TimeOfDay, TimeFlexibility


def create_measure(db: Session, data: MeasureBaseSchema):
    stmt = select(Measure).where(Measure.name == data.name)
    existing_measure = db.execute(stmt).scalar_one_or_none()

    if existing_measure:
        raise ValueError(f"Measure with name {data.name} already exists")

    try:
        measure = Measure(
            name=data.name,
            default_duration=data.default_duration,
            text=data.text,
            time_of_day=data.time_of_day,
            time_flexibility=data.time_flexibility,
        )

        db.add(measure)
        db.commit()
        db.refresh(measure)
        return measure

    except IntegrityError:
        db.rollback()
        raise


def get_measures(
    db: Session,
    query_str: Optional[str] = None,
    time_of_day: Optional[TimeOfDay] = None,
    time_flexibility: Optional[TimeFlexibility] = None,
    is_active: Optional[bool] = None,
    is_standard: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Measure]:
    query = select(Measure).order_by(Measure.created)

    if time_of_day is not None:
        query = query.where(Measure.time_of_day == time_of_day)

    if time_flexibility is not None:
        query = query.where(Measure.time_flexibility == time_flexibility)

    if is_active is not None:
        query = query.where(Measure.is_active == is_active)

    if is_standard is not None:
        query = query.where(Measure.is_standard == is_standard)

    if query_str is not None:
        query = query.where(Measure.name.ilike(f"%{query_str}%"))

    query = query.offset(skip).limit(limit)

    return list(db.execute(query).scalars().all())


def get_measure_by_id(
    db: Session, measure_id: int, include_inactive: bool = False
) -> Optional[Measure]:
    stmt = select(Measure).where(Measure.id == measure_id)

    if not include_inactive:
        stmt = stmt.where(Measure.is_active)

    measure = db.execute(stmt).scalar_one_or_none()

    return measure


def delete_measure(db: Session, measure_id: int) -> bool:
    stmt = select(Measure).where(Measure.id == measure_id)
    measure = db.execute(stmt).scalar_one_or_none()

    if not measure:
        return False

    try:
        db.delete(measure)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False
