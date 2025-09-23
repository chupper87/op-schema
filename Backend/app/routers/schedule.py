from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Query, Depends, HTTPException
from typing import Optional
from datetime import date as date_type

from ..dependencies import require_admin
from ..core.logger import logger
from ..models.auth import User
from ..schemas.relations import ScheduleMeasureCreateSchema, ScheduleMeasureOutSchema
from ..schemas.customer import CustomerOutSchema
from ..schemas.employee import EmployeeOutSchema
from ..schemas.schedule import (
    ScheduleOutSchema,
    ScheduleBaseSchema,
    ScheduleUpdateSchema,
)
from ..core.db_setup import get_db
from ..core.enums import ShiftType
from ..crud.schedule import (
    get_schedules,
    create_schedule,
    get_schedule_by_id,
    update_schedule,
    delete_schedule,
    duplicate_schedule,
    assign_employee_to_schedule,
    remove_employee_from_schedule,
    get_schedule_employees,
    assign_customer_to_schedule,
    remove_customer_from_schedule,
    get_schedule_customers,
    assign_measure_to_schedule,
    remove_measure_from_schedule,
    get_schedule_measures,
)

router = APIRouter(tags=["schedules"], prefix="/schedules")


@router.post(
    "/create-schedule",
    response_model=ScheduleOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_schedule_endpoint(
    data: ScheduleBaseSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        new_schedule = create_schedule(db, data)
        logger.info(
            f"New schedule {new_schedule.date} {new_schedule.shift_type} created"
        )
        return new_schedule
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=list[ScheduleOutSchema], status_code=status.HTTP_200_OK)
async def list_schedules(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    shift_type: Optional[ShiftType] = Query(None, description="Filter by shift type"),
    date: Optional[date_type] = Query(None, description="Filter by exact date"),
    start_date: Optional[date_type] = Query(None, description="Filter by start date"),
    end_date: Optional[date_type] = Query(None, description="Filter by end date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    schedules = get_schedules(
        db,
        skip=skip,
        limit=limit,
        shift_type=shift_type,
        date=date,
        start_date=start_date,
        end_date=end_date,
    )
    logger.info(
        f"Admin {current_user.username} listed {len(schedules)} schedules "
        f"(skip={skip}, limit={limit}, shift_type={shift_type}, date={date}, "
        f"start_date={start_date}, end_date={end_date})"
    )
    return schedules


@router.get(
    "/{schedule_id}", response_model=ScheduleOutSchema, status_code=status.HTTP_200_OK
)
async def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found",
        )
    return schedule


@router.patch(
    "/{schedule_id}", response_model=ScheduleOutSchema, status_code=status.HTTP_200_OK
)
async def update_schedule_endpoint(
    schedule_id: int,
    data: ScheduleUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    schedule = update_schedule(db, schedule_id, data)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found",
        )
    logger.info(f"Schedule {schedule_id} updated by admin {current_user.username}")
    return schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule_endpoint(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = delete_schedule(db, schedule_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule with ID {schedule_id} not found",
        )
    logger.info(f"Schedule {schedule_id} deleted by admin {current_user.username}")


@router.post(
    "/duplicate",
    response_model=ScheduleOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def duplicate_schedule_endpoint(
    source_date: date_type,
    target_date: date_type,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        new_schedule = duplicate_schedule(
            db, source_date=source_date, target_date=target_date
        )
        logger.info(f"Duplicated schedule from {source_date} to {target_date}")
        return new_schedule
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{schedule_id}/employees", status_code=status.HTTP_201_CREATED)
async def assign_employee_to_schedule_endpoint(
    schedule_id: int,
    employee_id: int = Query(..., description="Employee ID to assign"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        assign_employee_to_schedule(db, schedule_id, employee_id)
        logger.info(
            f"Admin {current_user.username} assigned employee {employee_id} to schedule {schedule_id}"
        )
        return {"message": "Employee assigned to schedule successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{schedule_id}/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def remove_employee_from_schedule_endpoint(
    schedule_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = remove_employee_from_schedule(db, schedule_id, employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found on schedule {schedule_id}",
        )
    logger.info(
        f"Admin {current_user.username} removed employee {employee_id} from schedule {schedule_id}"
    )


@router.get("/{schedule_id}/employees", response_model=list[EmployeeOutSchema])
async def get_schedule_employees_endpoint(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    employees = get_schedule_employees(db, schedule_id)
    return employees


@router.post("/{schedule_id}/customers", status_code=status.HTTP_201_CREATED)
async def assign_customer_to_schedule_endpoint(
    schedule_id: int,
    customer_id: int = Query(..., description="Customer ID to assign"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        assign_customer_to_schedule(db, schedule_id, customer_id)
        logger.info(
            f"Admin {current_user.username} assigned customer {customer_id} to schedule {schedule_id}"
        )
        return {"message": "Customer assigned to schedule successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{schedule_id}/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def remove_customer_from_schedule_endpoint(
    schedule_id: int,
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = remove_customer_from_schedule(db, schedule_id, customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer {customer_id} not found on schedule {schedule_id}",
        )
    logger.info(
        f"Admin {current_user.username} removed customer {customer_id} from schedule {schedule_id}"
    )


@router.get("/{schedule_id}/customers", response_model=list[CustomerOutSchema])
async def get_schedule_customers_endpoint(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    customers = get_schedule_customers(db, schedule_id)
    return customers


# Measure assignment endpoints
@router.post("/{schedule_id}/measures", status_code=status.HTTP_201_CREATED)
async def assign_measure_to_schedule_endpoint(
    schedule_id: int,
    data: ScheduleMeasureCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        assign_measure_to_schedule(db, schedule_id, data)
        logger.info(
            f"Admin {current_user.username} assigned measure {data.measure_id} to schedule {schedule_id}"
        )
        return {"message": "Measure assigned to schedule successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{schedule_id}/measures/{measure_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def remove_measure_from_schedule_endpoint(
    schedule_id: int,
    measure_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = remove_measure_from_schedule(db, schedule_id, measure_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measure {measure_id} not found on schedule {schedule_id}",
        )
    logger.info(
        f"Admin {current_user.username} removed measure {measure_id} from schedule {schedule_id}"
    )


@router.get("/{schedule_id}/measures", response_model=list[ScheduleMeasureOutSchema])
async def get_schedule_measures_endpoint(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    measures = get_schedule_measures(db, schedule_id)
    return measures
