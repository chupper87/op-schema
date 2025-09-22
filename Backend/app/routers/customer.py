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
