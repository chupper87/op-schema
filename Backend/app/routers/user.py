from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..models import User, Employee
from ..core.db_setup import get_db
from ..core.security import get_password_hash
from ..schemas.user import UserRegisterSchema, UserOutSchema

router = APIRouter(tags=["user"], prefix="/user")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserRegisterSchema, db: Session = Depends(get_db)
) -> UserOutSchema:  # type: ignore
    hashed_password = get_password_hash(user.password)

    new_employee = Employee(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        gender=user.gender,
        is_active=True,
        birth_date=user.birth_date,
    )
    db.add(new_employee)
    db.flush()

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        employee_id=new_employee.id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserOutSchema.model_validate(new_user)
