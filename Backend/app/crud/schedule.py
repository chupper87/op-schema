from typing import Optional
from datetime import date as date_type
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from ..schemas.schedule import ScheduleBaseSchema, ScheduleUpdateSchema
from ..schemas.relations import ScheduleMeasureCreateSchema
from ..models.schedule import (
    Schedule,
    ScheduleEmployee,
    ScheduleCustomer,
    ScheduleMeasure,
)

from ..models.auth import User
from ..models.customer import Customer
from ..core.exceptions import (
    ScheduleNotFoundError,
    EmployeeNotFoundError,
    MeasureNotFoundError,
)
from ..models.measure import Measure
from ..core.enums import ShiftType
from ..core.exceptions import CustomerNotFoundError


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


def update_schedule(
    db: Session, schedule_id: int, data: ScheduleUpdateSchema
) -> Optional[Schedule]:
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
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
    try:
        db.delete(schedule)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise


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


def assign_employee_to_schedule(
    db: Session, schedule_id: int, employee_id: int
) -> None:
    # Verify schedule exists
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        raise ScheduleNotFoundError(schedule_id)

    # Verify employee exists
    employee_stmt = (
        select(User).join(User.employee).where(User.employee.id == employee_id)
    )
    employee = db.execute(employee_stmt).scalar_one_or_none()
    if not employee:
        raise EmployeeNotFoundError(employee_id)

    # Check if assignment already exists
    existing = db.execute(
        select(ScheduleEmployee).where(
            ScheduleEmployee.schedule_id == schedule_id,
            ScheduleEmployee.employee_id == employee_id,
        )
    ).scalar_one_or_none()

    if existing:
        raise ValueError(
            f"Employee {employee_id} already assigned to schedule {schedule_id}"
        )

    try:
        assignment = ScheduleEmployee(schedule_id=schedule_id, employee_id=employee_id)
        db.add(assignment)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise


def remove_employee_from_schedule(
    db: Session, schedule_id: int, employee_id: int
) -> bool:
    assignment = db.execute(
        select(ScheduleEmployee).where(
            ScheduleEmployee.schedule_id == schedule_id,
            ScheduleEmployee.employee_id == employee_id,
        )
    ).scalar_one_or_none()

    if not assignment:
        return False

    try:
        db.delete(assignment)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise


def get_schedule_employees(db: Session, schedule_id: int) -> list[User]:
    employees = (
        db.execute(
            select(User)
            .join(User.employee)
            .join(ScheduleEmployee, ScheduleEmployee.employee_id == User.employee.id)
            .where(ScheduleEmployee.schedule_id == schedule_id)
        )
        .scalars()
        .all()
    )

    return list(employees)


def assign_customer_to_schedule(
    db: Session, schedule_id: int, customer_id: int
) -> None:
    # Verify schedule exists
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        raise ScheduleNotFoundError(schedule_id)

    # Verify customer exists
    customer_stmt = select(Customer).where(Customer.id == customer_id)
    customer = db.execute(customer_stmt).scalar_one_or_none()
    if not customer:
        raise CustomerNotFoundError(customer_id)  # Not EmployeeNotFoundError

    existing = db.execute(
        select(ScheduleCustomer).where(
            ScheduleCustomer.schedule_id == schedule_id,
            ScheduleCustomer.customer_id == customer_id,
        )
    ).scalar_one_or_none()

    if existing:
        raise ValueError(
            f"Customer {customer_id} already assigned to schedule {schedule_id}"
        )

    try:
        assignment = ScheduleCustomer(schedule_id=schedule_id, customer_id=customer_id)
        db.add(assignment)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise


def remove_customer_from_schedule(
    db: Session, schedule_id: int, customer_id: int
) -> bool:
    assignment = db.execute(
        select(ScheduleCustomer).where(
            ScheduleCustomer.schedule_id == schedule_id,
            ScheduleCustomer.customer_id == customer_id,
        )
    ).scalar_one_or_none()

    if not assignment:
        return False

    try:
        db.delete(assignment)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise


def get_schedule_customers(db: Session, schedule_id: int) -> list[Customer]:
    customers = (
        db.execute(
            select(Customer)
            .join(ScheduleCustomer, ScheduleCustomer.customer_id == Customer.id)
            .where(ScheduleCustomer.schedule_id == schedule_id)
        )
        .scalars()
        .all()
    )

    return list(customers)


def assign_measure_to_schedule(
    db: Session, schedule_id: int, data: ScheduleMeasureCreateSchema
) -> None:
    # Verify schedule exists
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        raise ScheduleNotFoundError(schedule_id)

    # Verify measure exists
    measure_stmt = select(Measure).where(Measure.id == data.measure_id)
    measure = db.execute(measure_stmt).scalar_one_or_none()
    if not measure:
        raise MeasureNotFoundError(data.measure_id)

    # Check if assignment already exists
    existing = db.execute(
        select(ScheduleMeasure).where(
            ScheduleMeasure.schedule_id == schedule_id,
            ScheduleMeasure.measure_id == data.measure_id,
        )
    ).scalar_one_or_none()

    if existing:
        raise ValueError(
            f"Measure {data.measure_id} already assigned to schedule {schedule_id}"
        )

    try:
        assignment = ScheduleMeasure(
            schedule_id=schedule_id,
            measure_id=data.measure_id,
            time_of_day=data.time_of_day,
            custom_duration=data.custom_duration,
            notes=data.notes,
        )
        db.add(assignment)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise


def remove_measure_from_schedule(
    db: Session, schedule_id: int, measure_id: int
) -> bool:
    assignment = db.execute(
        select(ScheduleMeasure).where(
            ScheduleMeasure.schedule_id == schedule_id,
            ScheduleMeasure.measure_id == measure_id,
        )
    ).scalar_one_or_none()

    if not assignment:
        return False

    try:
        db.delete(assignment)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise


def get_schedule_measures(db: Session, schedule_id: int) -> list[ScheduleMeasure]:
    measures = (
        db.execute(
            select(ScheduleMeasure).where(ScheduleMeasure.schedule_id == schedule_id)
        )
        .scalars()
        .all()
    )

    return list(measures)
