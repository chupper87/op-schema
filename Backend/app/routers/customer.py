from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..core.db_setup import get_db
from ..core.security import RoleChecker, RoleType
from ..core.logger import logger
from ..schemas.customer import CustomerOutSchema, CustomerBaseSchema
from ..models.auth import User
from ..crud.customer import create_customer, get_customers, get_customer_by_id


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
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    customers = get_customers(
        db=db, skip=skip, limit=limit, include_inactive=include_inactive
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
