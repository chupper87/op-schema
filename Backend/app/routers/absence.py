from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from sqlalchemy.exc import IntegrityError

from ..schemas.absence import AbsenceBaseSchema, AbsenceUpdateSchema, AbsenceOutSchema
from ..core.enums import AbsenceType
from ..models.auth import User
from ..crud.absence import (
    create_absence,
    get_absences,
    update_absence,
    delete_absence,
    get_absence_by_id,
)
from ..core.db_setup import get_db
from ..dependencies import require_admin
from ..core.logger import logger


router = APIRouter(prefix="/absences", tags=["Absences"])


@router.post("/", response_model=AbsenceOutSchema, status_code=status.HTTP_201_CREATED)
async def create_absence_endpoint(
    data: AbsenceBaseSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        new_absence = create_absence(db, data)
        logger.info(f"{current_user.username} created a new absence: {new_absence.id}")
        return new_absence
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Database constraint violation"
        )


@router.get("/", response_model=list[AbsenceOutSchema], status_code=status.HTTP_200_OK)
async def list_absences(
    employee_id: Optional[int] = Query(None, description="Filter by employee"),
    absence_type: Optional[AbsenceType] = Query(
        None, description="Filter by absence type"
    ),
    start_date: Optional[date] = Query(None, description="Filter from start date"),
    end_date: Optional[date] = Query(None, description="Filter to end date"),
    active_only: Optional[bool] = Query(None, description="Show only current absences"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    absences = get_absences(
        db=db,
        employee_id=employee_id,
        absence_type=absence_type,
        start_date=start_date,
        end_date=end_date,
        active_only=active_only,
        skip=skip,
        limit=limit,
    )
    logger.info(
        f"Admin {current_user.username} listed {len(absences)} absences "
        f"(skip={skip}, limit={limit})"
    )
    return absences


@router.get(
    "/{absence_id}", response_model=AbsenceOutSchema, status_code=status.HTTP_200_OK
)
async def get_absence(
    absence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    absence = get_absence_by_id(db, absence_id=absence_id)

    if not absence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Absence with ID {absence_id} not found",
        )

    return absence


@router.patch(
    "/{absence_id}", response_model=AbsenceOutSchema, status_code=status.HTTP_200_OK
)
async def update_absence_endpoint(
    absence_id: int,
    data: AbsenceUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        absence = update_absence(db, absence_id=absence_id, data=data)

        if not absence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Absence with ID {absence_id} not found",
            )

        logger.info(f"Admin {current_user.username} updated absence {absence_id}")
        return absence

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Database constraint violation"
        )


@router.delete("/{absence_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_absence_endpoint(
    absence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    logger.info(f"Admin {current_user.username} is deleting absence {absence_id}")

    try:
        success = delete_absence(db, absence_id=absence_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Absence with ID {absence_id} not found",
            )

        logger.info(f"Absence {absence_id} was deleted by {current_user.username}")

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete absence {absence_id} - it may be referenced by other records",
        )
