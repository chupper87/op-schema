from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..models.customer import CustomerMeasure
from ..schemas.relations import CustomerMeasureCreateSchema


def get_customer_measures(db: Session, customer_id: int) -> list[CustomerMeasure]:
    """
    Hämtar alla insatser (measures) kopplade till en specifik kund.

    Använder SQLAlchemy relationship för att automatiskt ladda measure-information.
    CustomerMeasure.measure ger tillgång till Measure-objektet.

    Args:
        db: Databas session
        customer_id: ID för kunden vars insatser ska hämtas

    Returns:
        Lista med CustomerMeasure-objekt, sorterade efter skapandedatum
    """
    stmt = (
        select(CustomerMeasure)
        .where(CustomerMeasure.customer_id == customer_id)
        .order_by(CustomerMeasure.created)
    )

    return list(db.execute(stmt).scalars().all())


def create_customer_measure(
    db: Session, customer_id: int, data: CustomerMeasureCreateSchema
) -> CustomerMeasure:
    """
    Skapar en ny koppling mellan kund och insats med kundspecifika inställningar.

    Args:
        db: Databas session
        customer_id: ID för kunden som ska kopplas till insatsen
        data: Schema med insatsdata (measure_id, duration, frequency, etc.)

    Returns:
        Skapad CustomerMeasure med auto-genererat ID

    Raises:
        IntegrityError: Om measure_id eller customer_id inte existerar,
                       eller om kombinationen redan finns (duplicate)
    """
    try:
        customer_measure = CustomerMeasure(
            customer_id=customer_id,
            measure_id=data.measure_id,
            customer_duration=data.customer_duration,
            frequency=data.frequency,
            days_of_week=data.days_of_week,
            occurrences_per_week=data.occurrences_per_week,
            customer_notes=data.customer_notes,
            customer_time_of_day=data.customer_time_of_day,
            customer_time_flexibility=data.customer_time_flexibility,
            schedule_info=data.schedule_info,
        )

        db.add(customer_measure)
        db.commit()
        db.refresh(customer_measure)

        return customer_measure

    except IntegrityError:
        db.rollback()
        raise


def delete_customer_measure(db: Session, customer_measure_id: int) -> bool:
    """
    Raderar en kundinsats-koppling permanent från databasen.

    Args:
        db: Databas session
        customer_measure_id: ID för customer_measure som ska raderas

    Returns:
        True om customer_measure hittades och raderades
        False om customer_measure_id inte existerar

    Raises:
        IntegrityError: Om customer_measure används i andra tabeller
                       (t.ex. refererad i schedules)
    """
    stmt = select(CustomerMeasure).where(CustomerMeasure.id == customer_measure_id)
    customer_measure = db.execute(stmt).scalar_one_or_none()

    if not customer_measure:
        return False

    try:
        db.delete(customer_measure)
        db.commit()
        return True

    except IntegrityError:
        db.rollback()
        raise
