from random import SystemRandom
from typing import Annotated, List
from uuid import UUID
from datetime import datetime, UTC
import base64
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from models.auth import Token, User
from enums import RoleType
from db_setup import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEFAULT_ENTROPY = 32
_sysrand = SystemRandom()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# Token


def token_bytes(nbytes=None):
    if nbytes is None:
        nbytes = DEFAULT_ENTROPY
    return _sysrand.randbytes(nbytes)


def token_url_safe(nbytes=None):
    tok = token_bytes(nbytes)
    return base64.urlsafe_b64encode(tok).rstrip(b"=").decode("ascii")


def create_database_token(user_id: UUID, db: Session):
    randomized_token = token_url_safe()
    new_token = Token(token=randomized_token, user_id=user_id)
    db.add(new_token)
    db.commit()
    return new_token


def verify_token_access(token_str: str, db: Session) -> Token:
    current_time = datetime.now(UTC)

    token = db.execute(select(Token).where(Token.token == token_str)).scalars().first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expire_date = (
        token.expire_date.replace(tzinfo=UTC)
        if token.expire_date.tzinfo is None
        else token.expire_date
    )

    if expire_date <= current_time:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


async def get_current_token(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    """
    oauth2_scheme automatically extracts the token from the authentication header
    Used when we simply want to return the token, instead of returning a user. E.g for logout
    """
    token = verify_token_access(token_str=token, db=db)
    return token


# User


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    """
    oauth2_scheme automatically extracts the token from the authentication header
    Below, we get the current user based on that token
    """
    token = verify_token_access(token_str=token, db=db)
    user = token.user
    return user


def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency that verifies the current user is a superuser.
    Returns the user object if the user is a superuser,
    otherwise raises an HTTP 403 Forbidden exception.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Superuser privileges required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


class RoleChecker:
    def __init__(self, allowed_roles: List[RoleType]):
        pass
