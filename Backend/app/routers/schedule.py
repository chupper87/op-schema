from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Query, Depends, HTTPException
from typing import Optional
from datetime import date as date_type

from ..core.logger import logger
from ..models.auth import User
from ..schemas.schedule import (
    ScheduleOutSchema,
    ScheduleBaseSchema,
    ScheduleUpdateSchema,
)
from ..core.db_setup import get_db
from ..core.enums import RoleType, ShiftType
from ..core.security import RoleChecker
from ..crud.schedule import (
    get_schedules,
    create_schedule,
    get_schedule_by_id,
    update_schedule,
    delete_schedule,
)

router = APIRouter(tags=["schedules"], prefix="/schedules")

require_admin = RoleChecker([RoleType.ADMIN])


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
    date: Optional[date_type] = Query(None, description="Filter by date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    schedules = get_schedules(
        db, skip=skip, limit=limit, shift_type=shift_type, date=date
    )
    logger.info(
        f"Admin {current_user.username} listed {len(schedules)} schedules "
        f"(skip={skip}, limit={limit}, shift_type={shift_type}, date={date})"
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
    schedule = update_schedule(db, schedule_id, data.model_dump(exclude_unset=True))
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
