from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError

from ..schemas.customer import CustomerBaseSchema, CustomerUpdateSchema
from ..models.customer import Customer
from ..core.enums import CareLevel


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
    db: Session,
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
    key_number: str | None = None,
) -> list[Customer]:
    query = select(Customer).order_by(Customer.created).offset(skip).limit(limit)

    if not include_inactive:
        query = query.where(Customer.is_active)

    if key_number:
        query = query.where(Customer.key_number == key_number)

    return list(db.execute(query).scalars().all())


def get_customer_by_id(
    db: Session, customer_id: int, include_inactive: bool = False
) -> Optional[Customer]:
    stmt = select(Customer).where(Customer.id == customer_id)

    if not include_inactive:
        stmt = stmt.where(Customer.is_active)

    customer = db.execute(stmt).scalar_one_or_none()
    return customer


def delete_customer(db: Session, customer_id: int) -> bool:
    stmt = select(Customer).where(Customer.id == customer_id)
    customer = db.execute(stmt).scalar_one_or_none()

    if not customer:
        return False

    db.delete(customer)
    db.commit()
    return True


def deactivate_customer(db: Session, customer_id: int) -> bool:
    stmt = select(Customer).where(Customer.id == customer_id)

    customer = db.execute(stmt).scalar_one_or_none()

    if not customer:
        return False

    if not customer.is_active:
        return False

    customer.is_active = False
    db.commit()
    return True


def activate_customer(db: Session, customer_id: int) -> bool:
    stmt = select(Customer).where(Customer.id == customer_id)

    customer = db.execute(stmt).scalar_one_or_none()

    if not customer:
        return False

    if customer.is_active:
        return False

    customer.is_active = True
    db.commit()
    return True


def update_customer(
    db: Session, customer_id: int, data: CustomerUpdateSchema
) -> Optional[Customer]:
    stmt = select(Customer).where(Customer.id == customer_id)
    customer = db.execute(stmt).scalar_one_or_none()

    if not customer:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)

    try:
        db.commit()
        db.refresh(customer)
        return customer
    except IntegrityError:
        db.rollback()
        raise


def search_customers(
    db: Session,
    query: str | None = None,
    care_level: CareLevel | None = None,
    is_active: bool | None = None,
) -> list[Customer]:
    stmt = select(Customer)

    if query:
        # Build search conditions for text fields
        text_conditions = [
            Customer.first_name.ilike(f"%{query}%"),
            Customer.last_name.ilike(f"%{query}%"),
            Customer.address.ilike(f"%{query}%"),
        ]

        try:
            key_number_query = int(query)
            stmt = stmt.where(
                or_(*text_conditions, Customer.key_number == key_number_query)
            )
        except ValueError:
            stmt = stmt.where(or_(*text_conditions))

    if care_level:
        stmt = stmt.where(Customer.care_level == care_level)

    if is_active is not None:
        stmt = stmt.where(Customer.is_active == is_active)

    return list(db.execute(stmt).scalars().all())


def customer_exists(db: Session, key_number: int) -> bool:
    stmt = select(Customer).where(Customer.key_number == key_number)
    return db.execute(stmt).scalar_one_or_none() is not None
