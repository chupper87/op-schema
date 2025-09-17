from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..core.db_setup import get_db
from ..core.security import RoleChecker, RoleType
from ..core.logger import logger
from ..core.enums import CareLevel
from ..schemas.customer import (
    CustomerOutSchema,
    CustomerBaseSchema,
    CustomerUpdateSchema,
)
from ..models.auth import User
from ..crud.customer import (
    activate_customer,
    create_customer,
    deactivate_customer,
    delete_customer,
    get_customers,
    get_customer_by_id,
    update_customer,
    search_customers,
    customer_exists,
)


router = APIRouter(tags=["customer"], prefix="/customers")

require_admin = RoleChecker([RoleType.ADMIN])


@router.post(
    "/create-customer",
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
        logger.info(
            f"New customer {new_customer.first_name} {new_customer.last_name} created with id={new_customer.id}, key={new_customer.key_number}"
        )

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
        f"(skip={skip}, limit={limit}, include_inactive={include_inactive}, key_number={key_number})"
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


@router.delete("/{customer_id}", status_code=status.HTTP_200_OK)
async def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    logger.info(f"Admin {current_user.username} is deleting customer {customer_id}")

    success = delete_customer(db, customer_id=customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )

    logger.info(
        f"Customer {customer_id} permanently deleted by admin {current_user.username}"
    )
    return {"detail": f"Customer {customer_id} has been permanently deleted"}


@router.put("/{customer_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = deactivate_customer(db, customer_id=customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found or already inactive",
        )

    logger.info(
        f"Customer {customer_id} deactivated successfully by admin {current_user.username}"
    )


@router.put("/{customer_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = activate_customer(db, customer_id=customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found or already active",
        )

    logger.info(
        f"Customer {customer_id} activated successfully by admin {current_user.username}"
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

    if not customers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No customers found",
        )

    logger.info(f"Found {len(customers)} customer(s) for query='{q}'")

    return customers


@router.get("/exists/{key_number}", status_code=status.HTTP_200_OK)
async def check_customer_exists(
    key_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    exists = customer_exists(db, key_number=key_number)
    return {"exists": exists}
