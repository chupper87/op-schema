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
