from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date as date_type

from ..core.enums import VisitStatus
from ..models.care_visit import CareVisit
from ..schemas.care_visit import CareVisitBaseSchema, CareVisitUpdateSchema


def create_care_visit(db: Session, data: CareVisitBaseSchema) -> CareVisit:
    try:
        care_visit = CareVisit(
            date=data.date,
            status=data.status,
            duration=data.duration,
            notes=data.notes,
            schedule_id=data.schedule_id,
            customer_id=data.customer_id,
        )
        db.add(care_visit)
        db.commit()
        db.refresh(care_visit)
        return care_visit
    except IntegrityError:
        db.rollback()
        raise


def get_care_visits(
    db: Session,
    date: Optional[date_type] = None,
    start_date: Optional[date_type] = None,
    end_date: Optional[date_type] = None,
    status: Optional[VisitStatus] = None,
    customer_id: Optional[int] = None,
    schedule_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[CareVisit]:
    query = select(CareVisit).order_by(CareVisit.date)

    if date is not None:
        query = query.where(CareVisit.date == date)

    if start_date is not None:
        query = query.where(CareVisit.date >= start_date)

    if end_date is not None:
        query = query.where(CareVisit.date <= end_date)

    if status is not None:
        query = query.where(CareVisit.status == status)

    if customer_id is not None:
        query = query.where(CareVisit.customer_id == customer_id)

    if schedule_id is not None:
        query = query.where(CareVisit.schedule_id == schedule_id)

    query = query.offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())


def get_care_visit_by_id(db: Session, care_visit_id: int) -> Optional[CareVisit]:
    stmt = select(CareVisit).where(CareVisit.id == care_visit_id)
    return db.execute(stmt).scalar_one_or_none()


def delete_care_visit(db: Session, care_visit_id: int) -> bool:
    stmt = select(CareVisit).where(CareVisit.id == care_visit_id)
    care_visit = db.execute(stmt).scalar_one_or_none()

    if not care_visit:
        return False

    try:
        db.delete(care_visit)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise


def update_care_visit(
    db: Session, care_visit_id: int, data: CareVisitUpdateSchema
) -> Optional[CareVisit]:
    stmt = select(CareVisit).where(CareVisit.id == care_visit_id)
    care_visit = db.execute(stmt).scalar_one_or_none()

    if not care_visit:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(care_visit, field, value)

    try:
        db.commit()
        db.refresh(care_visit)
        return care_visit
    except IntegrityError:
        db.rollback()
        raise


def get_upcoming_visits(
    db: Session,
    customer_id: Optional[int] = None,
    schedule_id: Optional[int] = None,
    days_ahead: int = 7,
    skip: int = 0,
    limit: int = 100,
) -> list[CareVisit]:
    """Get upcoming visits within specified days"""
    from datetime import datetime, timedelta

    today = datetime.now().date()
    future_date = today + timedelta(days=days_ahead)

    return get_care_visits(
        db=db,
        start_date=today,
        end_date=future_date,
        status=VisitStatus.PLANNED,  # Assuming you have this enum value
        customer_id=customer_id,
        schedule_id=schedule_id,
        skip=skip,
        limit=limit,
    )


def get_completed_visits(
    db: Session,
    customer_id: Optional[int] = None,
    schedule_id: Optional[int] = None,
    days_back: int = 30,
    skip: int = 0,
    limit: int = 100,
) -> list[CareVisit]:
    """Get completed visits from recent period"""
    from datetime import datetime, timedelta

    today = datetime.now().date()
    past_date = today - timedelta(days=days_back)

    return get_care_visits(
        db=db,
        start_date=past_date,
        end_date=today,
        status=VisitStatus.COMPLETED,
        customer_id=customer_id,
        schedule_id=schedule_id,
        skip=skip,
        limit=limit,
    )


def get_overdue_visits(
    db: Session,
    customer_id: Optional[int] = None,
    schedule_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[CareVisit]:
    """Get visits that should have been completed but weren't"""
    from datetime import datetime

    yesterday = datetime.now().date()

    return get_care_visits(
        db=db,
        end_date=yesterday,
        status=VisitStatus.PLANNED,  # Still scheduled but past due
        customer_id=customer_id,
        schedule_id=schedule_id,
        skip=skip,
        limit=limit,
    )
