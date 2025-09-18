from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..schemas.measure import MeasureBaseSchema
from ..models.measure import Measure


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
