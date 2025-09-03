from typing import Any, Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..core.db_setup import get_db
from ..core.security import get_password_hash, RoleChecker
from ..core.enums import RoleType
from ..schemas.user import UserRegisterSchema, UserOutSchema
from ..schemas.token import Token
from ..models import User


router = APIRouter(tags=["auth"], prefix="/auth")

require_admin = RoleChecker([RoleType.ADMIN])


# Token login


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:  # type: ignore
    # user = db.execute(select(User).where(User.email == form_data.username))

    pass


# User routes


@router.post("/users/create", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserRegisterSchema, db: Session = Depends(get_db)
) -> UserOutSchema:  # type: ignore
    pass
    # hashed_password = get_password_hash(user.password)
