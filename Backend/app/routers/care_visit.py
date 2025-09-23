from typing import Optional
from datetime import date as date_type
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, status, Depends, HTTPException, Query


from ..core.enums import VisitStatus
from ..core.logger import logger
from ..core.db_setup import get_db
from ..crud.care_visit import (
    create_care_visit,
    get_care_visits,
    get_care_visit_by_id,
    delete_care_visit,
    update_care_visit,
    get_upcoming_visits,
    get_completed_visits,
    get_overdue_visits,
)
from ..schemas.care_visit import (
    CareVisitBaseSchema,
    CareVisitOutSchema,
    CareVisitUpdateSchema,
)
from ..models.auth import User
from ..dependencies import require_admin


router = APIRouter(tags=["care_visit"], prefix="/care_visits")


@router.post(
    "/", response_model=CareVisitOutSchema, status_code=status.HTTP_201_CREATED
)
async def create_care_visit_endpoint(
    data: CareVisitBaseSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        new_care_visit = create_care_visit(db, data)
        logger.info(
            f"{current_user.username} created a new care_visit: {new_care_visit.id}"
        )

        return new_care_visit
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get(
    "/", response_model=list[CareVisitOutSchema], status_code=status.HTTP_200_OK
)
async def list_care_visits(
    date: Optional[date_type] = Query(None, description="Filter by exact date"),
    start_date: Optional[date_type] = Query(None, description="Filter from date"),
    end_date: Optional[date_type] = Query(None, description="Filter to date"),
    status: Optional[VisitStatus] = Query(None, description="Filter by visit status"),
    customer_id: Optional[int] = Query(None, description="Filter by customer"),
    schedule_id: Optional[int] = Query(None, description="Filter by schedule"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    care_visits = get_care_visits(
        db=db,
        date=date,
        start_date=start_date,
        end_date=end_date,
        status=status,
        customer_id=customer_id,
        schedule_id=schedule_id,
        skip=skip,
        limit=limit,
    )

    logger.info(
        f"Admin {current_user.username} listed {len(care_visits)} care visits "
        f"(skip={skip}, limit={limit})"
    )

    return care_visits


@router.get(
    "/{care_visit_id}",
    response_model=CareVisitOutSchema,
    status_code=status.HTTP_200_OK,
)
async def get_care_visit(
    care_visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    care_visit = get_care_visit_by_id(db, care_visit_id=care_visit_id)

    if not care_visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carevisit with ID {care_visit_id} not found",
        )

    return care_visit


@router.delete("/{care_visit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_care_visit_endpoint(
    care_visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    logger.info(f"Admin {current_user.username} is deleting measure {care_visit_id}")

    try:
        success = delete_care_visit(db, care_visit_id=care_visit_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Carevisit with ID {care_visit_id} not found",
            )

        logger.info(f"Carevisit {care_visit_id} was deleted by {current_user.username}")

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete carevisit {care_visit_id} - it may be referenced by other records",
        )


@router.patch(
    "/{care_visit_id}",
    response_model=CareVisitUpdateSchema,
    status_code=status.HTTP_200_OK,
)
async def update_care_visit_endpoint(
    care_visit_id: int,
    data: CareVisitUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    care_visit = update_care_visit(db, care_visit_id=care_visit_id, data=data)

    if not care_visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carevisit with ID {care_visit} not found",
        )

    logger.info(f"Admin {current_user.username} updated carevisit: {care_visit.id}")

    return care_visit


@router.get(
    "/upcoming/",
    response_model=list[CareVisitOutSchema],
    status_code=status.HTTP_200_OK,
)
async def list_upcoming_care_visits(
    customer_id: Optional[int] = Query(None, description="Filter by customer"),
    schedule_id: Optional[int] = Query(None, description="Filter by schedule"),
    days_ahead: int = Query(7, ge=1, le=90, description="Number of days ahead to look"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    care_visits = get_upcoming_visits(
        db=db,
        customer_id=customer_id,
        schedule_id=schedule_id,
        days_ahead=days_ahead,  # Pass the parameter through
        skip=skip,
        limit=limit,
    )
    logger.info(
        f"Admin {current_user.username} listed {len(care_visits)} upcoming care visits "
        f"({days_ahead} days ahead, skip={skip}, limit={limit})"
    )
    return care_visits


@router.get(
    "/completed/",
    response_model=list[CareVisitOutSchema],
    status_code=status.HTTP_200_OK,
)
async def list_completed_care_visits(
    customer_id: Optional[int] = Query(None, description="Filter by customer"),
    schedule_id: Optional[int] = Query(None, description="Filter by schedule"),
    days_back: int = Query(30, ge=1, le=365, description="Number of days back to look"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    care_visits = get_completed_visits(
        db=db,
        customer_id=customer_id,
        schedule_id=schedule_id,
        days_back=days_back,
        skip=skip,
        limit=limit,
    )

    logger.info(
        f"Admin {current_user.username} listed {len(care_visits)} completed care visits "
        f"({days_back} days back, skip={skip}, limit={limit})"
    )

    return care_visits


@router.get(
    "/overdue/", response_model=list[CareVisitOutSchema], status_code=status.HTTP_200_OK
)
async def list_overdue_care_visits(
    customer_id: Optional[int] = Query(None, description="Filter by customer"),
    schedule_id: Optional[int] = Query(None, description="Filter by schedule"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    care_visits = get_overdue_visits(
        db=db,
        customer_id=customer_id,
        schedule_id=schedule_id,
        skip=skip,
        limit=limit,
    )

    logger.info(
        f"Admin {current_user.username} listed {len(care_visits)} overdue care visits "
        f"(skip={skip}, limit={limit})"
    )

    return care_visits
