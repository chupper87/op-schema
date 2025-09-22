from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, status, Depends, HTTPException, Query

from ..models.auth import User
from ..core.logger import logger
from ..core.enums import TimeOfDay, TimeFlexibility
from ..core.db_setup import get_db
from ..core.exceptions import MeasureNotFoundError
from ..crud.measure import (
    create_measure,
    get_measures,
    get_measure_by_id,
    delete_measure,
    update_measure,
    set_measure_status,
)
from ..schemas.measure import (
    MeasureOutSchema,
    MeasureBaseSchema,
    MeasureUpdateSchema,
    MeasureStatusUpdateSchema,
)
from ..dependencies import require_admin


router = APIRouter(tags=["measure"], prefix="/measures")


@router.post(
    "/create-measure",
    response_model=MeasureOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_measure_endpoint(
    data: MeasureBaseSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        new_measure = create_measure(db, data)
        logger.info(
            f"{current_user.username} created a new measure: {new_measure.name}"
        )
        return new_measure
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Measure with name '{data.name}' already exists",
        )


@router.get("/", response_model=list[MeasureOutSchema], status_code=status.HTTP_200_OK)
async def list_measures(
    query_str: Optional[str] = Query(None, description="Search measures by name"),
    time_of_day: Optional[TimeOfDay] = Query(None, description="Filter by time of day"),
    time_flexibility: Optional[TimeFlexibility] = Query(
        None, description="Filter by time flexibility"
    ),
    is_active: Optional[bool] = Query(None, description="Filter by active/inactive"),
    is_standard: Optional[bool] = Query(
        None, description="Filter by standard vs custom measures"
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    measures = get_measures(
        db,
        query_str=query_str,
        time_of_day=time_of_day,
        time_flexibility=time_flexibility,
        is_active=is_active,
        is_standard=is_standard,
        skip=skip,
        limit=limit,
    )

    logger.info(
        f"Admin {current_user.username} listed {len(measures)} measures "
        f"(skip={skip}, limit={limit}, query_str={query_str}, "
        f"time_of_day={time_of_day}, time_flexibility={time_flexibility}, "
        f"is_active={is_active}, is_standard={is_standard})"
    )

    return measures


@router.get("/{measure_id}", status_code=status.HTTP_200_OK)
async def get_measure(
    measure_id: int,
    include_inactive: bool = Query(False, description="Include inactive measures"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    measure = get_measure_by_id(
        db, measure_id=measure_id, include_inactive=include_inactive
    )

    if not measure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measure with ID {measure_id} not found",
        )

    return measure


@router.delete("/{measure_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measure_endpoint(
    measure_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    logger.info(f"Admin {current_user.username} is deleting measure {measure_id}")

    success = delete_measure(db, measure_id=measure_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measure with ID {measure_id} not found",
        )

    logger.info(f"Measure {measure_id} was deleted by {current_user.username}")


@router.patch(
    "/{measure_id}", response_model=MeasureUpdateSchema, status_code=status.HTTP_200_OK
)
async def update_measure_endpoint(
    measure_id: int,
    data: MeasureUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    measure = update_measure(db, measure_id=measure_id, data=data)

    if not measure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measure with ID {measure_id} not found",
        )

    logger.info(f"Admin {current_user.username} updated measure: {measure.name}")

    return measure


@router.put("/{measure_id}/status", response_model=MeasureBaseSchema)
async def set_measure_status_endpoint(
    measure_id: int,
    status_data: MeasureStatusUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        measure = set_measure_status(db, measure_id, status_data.is_active)
        logger.info(
            f"Admin {current_user.username} updated measure {measure_id} status"
        )
        return measure
    except MeasureNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measure with ID {measure_id} not found",
        )
