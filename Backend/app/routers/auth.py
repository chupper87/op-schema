from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..core.db_setup import get_db
from ..core.security import (
    RoleChecker,
    verify_password,
    create_database_token,
)
from ..core.enums import RoleType
from ..schemas.user import UserRegisterSchema, UserOutSchema
from ..models import User


router = APIRouter(tags=["auth"], prefix="/auth")

require_admin = RoleChecker([RoleType.ADMIN])


# Token login


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> dict[str, str]:
    user = (
        db.execute(select(User).where(User.username == form_data.username))
        .scalars()
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Passwords do not match",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_obj = create_database_token(user.id, db=db)
    return {"access_token": token_obj.token, "token_type": "bearer"}


# User routes


@router.post("/users/create", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserRegisterSchema, db: Session = Depends(get_db)
) -> UserOutSchema:  # type: ignore
    pass
    # hashed_password = get_password_hash(user.password)
