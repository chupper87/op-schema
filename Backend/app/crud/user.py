from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..core.logger import logger
from ..models import User, Employee, Token
from ..schemas.user import (
    UserInviteSchema,
    UserCompleteRegistrationSchema,
    UserLoginSchema,
)
from ..core.security import token_url_safe, get_password_hash, verify_password


def invite_user(db: Session, user_data: UserInviteSchema):
    stmt = select(User).where(User.email == user_data.email)
    if db.execute(stmt).scalar_one_or_none():
        raise ValueError(f"Email {user_data.email} already exists")

    try:
        registration_token = token_url_safe()

        new_user = User(
            email=user_data.email,
            is_superuser=user_data.is_superuser,
            registration_token=registration_token,
            is_active=False,
            registration_completed=False,
        )

        new_employee = Employee(user=new_user)

        db.add(new_employee)
        db.commit()

        logger.info(f"Created user invitation for {user_data.email}")

        return new_user
    except IntegrityError:
        db.rollback()
        raise


def complete_registration(db: Session, user_data: UserCompleteRegistrationSchema):
    stmt = select(User).where(User.registration_token == user_data.registration_token)
    existing_user = db.execute(stmt).scalar_one_or_none()

    if not existing_user:
        raise ValueError("Invalid registration token")

    if existing_user.registration_completed:
        raise ValueError("Registration already completed")

    try:
        existing_user.username = user_data.username
        existing_user.hashed_password = get_password_hash(user_data.password)
        existing_user.is_active = True
        existing_user.registration_completed = True
        existing_user.registration_token = None

        existing_user.employee.first_name = user_data.first_name
        existing_user.employee.last_name = user_data.last_name
        existing_user.employee.phone = user_data.phone
        existing_user.employee.gender = user_data.gender
        existing_user.employee.role = user_data.role
        existing_user.employee.birth_date = user_data.birth_date

        db.commit()
        return existing_user
    except IntegrityError:
        db.rollback()
        raise


def authenticate_user(db: Session, user_data: UserLoginSchema):
    stmt = select(User).where(User.username == user_data.username)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        return None

    verified_password = verify_password(user_data.password, user.hashed_password)

    if verified_password:
        return user
    return None


def logout_user(db: Session, token: Token) -> None:
    db.delete(token)
    db.commit()


def delete_user(db, user_id):
    pass


def deactivate_user(db, user_id):
    pass


def activate_user(db, user_id):
    pass


def get_users(
    db: Session, skip: int = 0, limit: int = 100, include_inactive: bool = False
) -> List[User]:
    query = select(User).offset(skip).limit(limit)

    if not include_inactive:
        query = query.where(User.is_active)

    users = db.execute(query).scalars().all()
    return list(users)


def get_user_by_id(db, user_id, include_inactive):
    print("test")
