from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..models import User, Employee
from ..core.db_setup import get_db
from ..core.security import get_password_hash
from ..core.logger import logger
from ..schemas.user import UserRegisterSchema, UserOutSchema

router = APIRouter(tags=["user"], prefix="/user")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserRegisterSchema, db: Session = Depends(get_db)
) -> UserOutSchema:  # type: ignore
    logger.info(f"Registering new user: {user.username}")

    if db.query(User).filter(User.username == user.username).first():
        logger.warning(f"Username already exists: {user.username}")
        raise HTTPException(status_code=400, detail="Username already exists")

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

    logger.success(f"User created: {new_user.username} (id={new_user.id})")

    return UserOutSchema.model_validate(new_user)
