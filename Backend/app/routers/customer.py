from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db_setup import get_db
from ..core.security import RoleChecker, RoleType
from ..core.logger import logger
from ..schemas.customer import CustomerOutSchema, CustomerBaseSchema
from ..models.auth import User
from ..crud.customer import create_customer


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
