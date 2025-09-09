from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from core.logger import logger
from models import User, Employee
from schemas.user import UserInviteSchema, UserCompleteRegistrationSchema
from core.security import token_url_safe, get_password_hash


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
