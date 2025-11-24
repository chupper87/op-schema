from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..dependencies import require_admin
from ..core.db_setup import get_db
from ..core.exceptions import CustomerNotFoundError
from ..core.logger import logger
from ..core.enums import CareLevel
from ..schemas.customer import (
    CustomerOutSchema,
    CustomerBaseSchema,
    CustomerUpdateSchema,
    CustomerStatusUpdateSchema,
)
from ..models.auth import User
from ..crud.customer import (
    create_customer,
    delete_customer,
    get_customers,
    get_customer_by_id,
    update_customer,
    search_customers,
    customer_exists,
    set_customer_status,
)
from ..crud.customer_measure import (
    create_customer_measure,
    delete_customer_measure,
    get_customer_measures,
)
from ..schemas.relations import (
    CustomerMeasureOutSchema,
    CustomerMeasureCreateSchema,
)


router = APIRouter(tags=["customer"], prefix="/customers")


@router.post(
    "/",
    response_model=CustomerOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_endpoint(
    data: CustomerBaseSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        new_customer = create_customer(db, data)
        logger.info(f"New customer created with id={new_customer.id}")

        return new_customer

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get("/", response_model=list[CustomerOutSchema], status_code=status.HTTP_200_OK)
async def list_customers(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    include_inactive: bool = Query(False, description="Include inactive customers"),
    key_number: str | None = Query(None, description="Filter by customer key_number"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    customers = get_customers(
        db=db,
        skip=skip,
        limit=limit,
        include_inactive=include_inactive,
        key_number=key_number,
    )
    logger.info(
        f"Admin {current_user.username} listed {len(customers)} customers "
        f"(skip={skip}, limit={limit}, include_inactive={include_inactive})"
    )
    return customers


@router.get(
    "/{customer_id}", response_model=CustomerOutSchema, status_code=status.HTTP_200_OK
)
async def get_customer(
    customer_id: int,
    include_inactive: bool = Query(False, description="Include inactive customers"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    customer = get_customer_by_id(
        db, customer_id=customer_id, include_inactive=include_inactive
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )

    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    logger.info(f"Admin {current_user.username} is deleting customer {customer_id}")

    try:
        success = delete_customer(db, customer_id=customer_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found",
            )

        logger.info(
            f"Customer {customer_id} permanently deleted by admin {current_user.username}"
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete customer {customer_id} - it may be referenced by other records",
        )


@router.patch(
    "/{customer_id}",
    response_model=CustomerOutSchema,
    status_code=status.HTTP_200_OK,
)
async def update_customer_endpoint(
    customer_id: int,
    data: CustomerUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    customer = update_customer(db, customer_id=customer_id, data=data)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )

    logger.info(
        f"Admin {current_user.username} updated customer {customer.first_name} {customer.last_name}"
    )

    return customer


@router.get(
    "/search", response_model=list[CustomerOutSchema], status_code=status.HTTP_200_OK
)
async def search_customers_endpoint(
    q: str | None = None,
    care_level: CareLevel | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    customers = search_customers(
        db, query=q, care_level=care_level, is_active=is_active
    )

    logger.info(f"Customer search performed: {len(customers)} results")
    return customers


@router.get("/exists/{key_number}", status_code=status.HTTP_200_OK)
async def check_customer_exists(
    key_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    exists = customer_exists(db, key_number=key_number)
    return {"exists": exists}


@router.put("/{customer_id}/status", response_model=CustomerBaseSchema)
async def set_customer_status_endpoint(
    customer_id: int,
    status_data: CustomerStatusUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        customer = set_customer_status(db, customer_id, status_data.is_active)
        return customer
    except CustomerNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )


# =============================================================================
# Customer Measures Endpoints
# Endpoints för att hantera insatser (measures) kopplade till kunder
# =============================================================================


@router.get(
    "/{customer_id}/measures",
    response_model=list[CustomerMeasureOutSchema],
    status_code=status.HTTP_200_OK,
)
async def get_customer_measures_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Hämtar alla insatser för en specifik kund.

    Path: GET /customers/{customer_id}/measures
    """
    measures = get_customer_measures(db, customer_id=customer_id)

    logger.info(
        f"Admin {current_user.username} retrieved {len(measures)} measures "
        f"for customer {customer_id}"
    )

    return measures


@router.post(
    "/{customer_id}/measures",
    response_model=CustomerMeasureOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_measure_endpoint(
    customer_id: int,
    data: CustomerMeasureCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Lägger till en insats till en kund.

    Path: POST /customers/{customer_id}/measures
    """
    try:
        customer_measure = create_customer_measure(
            db, customer_id=customer_id, data=data
        )

        logger.info(
            f"Admin {current_user.username} added measure {data.measure_id} "
            f"to customer {customer_id}"
        )

        return customer_measure

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Measure {data.measure_id} already exists for customer {customer_id} "
            f"or invalid measure_id/customer_id",
        )


@router.delete(
    "/{customer_id}/measures/{customer_measure_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customer_measure_endpoint(
    customer_id: int,
    customer_measure_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Tar bort en insats från en kund.

    Path: DELETE /customers/{customer_id}/measures/{customer_measure_id}
    """
    logger.info(
        f"Admin {current_user.username} is deleting customer_measure {customer_measure_id} "
        f"from customer {customer_id}"
    )

    success = delete_customer_measure(db, customer_measure_id=customer_measure_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer measure with ID {customer_measure_id} not found",
        )

    logger.info(
        f"Customer measure {customer_measure_id} deleted by {current_user.username}"
    )
