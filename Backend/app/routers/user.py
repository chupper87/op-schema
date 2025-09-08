from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import delete
from ..models import User, Employee, Token
from ..core.enums import RoleType
from ..core.db_setup import get_db
from ..core.security import get_password_hash, RoleChecker
from ..core.logger import logger
from ..schemas.user import UserRegisterSchema, UserOutSchema

router = APIRouter(tags=["user"], prefix="/user")

require_admin = RoleChecker([RoleType.ADMIN])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserRegisterSchema, db: Session = Depends(get_db)
) -> UserOutSchema:
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


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    logger.info(f"Admin {current_user.username} is deleting user {user_id}")

    user = db.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    try:
        db.execute(delete(Token).where(Token.user_id == user_id))

        # Delete user
        employee_id = user.employee_id
        db.delete(user)

        employee = db.get(Employee, employee_id)
        if employee:
            db.delete(employee)

        db.commit()
        logger.success(f"User {user.username} (id={user.id}) deleted successfully")

    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to delete user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user",
        )
