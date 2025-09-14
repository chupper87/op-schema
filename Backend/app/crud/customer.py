from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..schemas.customer import CustomerBaseSchema
from ..models.customer import Customer


def create_customer(db: Session, data: CustomerBaseSchema) -> Customer:
    stmt = select(Customer).where(Customer.key_number == data.key_number)
    existing_customer = db.execute(stmt).scalar_one_or_none()

    if existing_customer:
        raise ValueError("Key number already exists")

    try:
        customer = Customer(
            first_name=data.first_name,
            last_name=data.last_name,
            key_number=data.key_number,
            address=data.address,
            care_level=data.care_level,
            gender=data.gender,
            approved_hours=data.approved_hours,
            is_active=data.is_active,
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    except IntegrityError:
        db.rollback()
        raise


def get_customers(
    db: Session, skip: int = 0, limit: int = 100, include_inactive: bool = False
) -> list[Customer]:
    query = select(Customer).order_by(Customer.created).offset(skip).limit(limit)

    if not include_inactive:
        query = query.where(Customer.is_active)

    return list(db.execute(query).scalars().all())


def get_customer_by_id(
    db: Session, customer_id: int, include_inactive: bool = False
) -> Optional[Customer]:
    stmt = select(Customer).where(Customer.id == customer_id)

    if not include_inactive:
        stmt = stmt.where(Customer.is_active)

    customer = db.execute(stmt).scalar_one_or_none()
    return customer
