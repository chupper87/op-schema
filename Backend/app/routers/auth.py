from typing import Annotated
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..core.logger import logger
from ..core.db_setup import get_db
from ..core.security import (
    RoleChecker,
    verify_password,
    create_database_token,
    get_current_token,
)
from ..core.enums import RoleType
from ..models import User, Token


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
        logger.warning(f"Failed login attempt: unknown user '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        logger.warning(
            f"Failed login attempt: wrong password for '{form_data.username}'"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Passwords do not match",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_obj = create_database_token(user.id, db=db)
    return {"access_token": token_obj.token, "token_type": "bearer"}


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_token: Token = Depends(get_current_token), db: Session = Depends(get_db)
):
    db.execute(delete(Token).where(Token.token == current_token.token))
    db.commit()

    logger.info(f"User with token {current_token.token} logged out")

    return
