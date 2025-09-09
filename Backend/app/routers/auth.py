from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..core.logger import logger
from ..core.db_setup import get_db
from ..core.security import (
    get_current_token,
    get_current_superuser,
    create_database_token,
)
from ..models import User, Token
from ..schemas.user import (
    UserCompleteRegistrationSchema,
    UserOutSchema,
    UserInviteSchema,
    UserLoginSchema,
)
from ..crud.user import (
    complete_registration,
    authenticate_user,
    invite_user,
    logout_user,
)
from ..services.email_service import EmailService

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/invite", status_code=status.HTTP_201_CREATED)
async def invite_user_endpoint(
    user_data: UserInviteSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    new_user = invite_user(db, user_data)

    if not new_user.registration_token:
        raise HTTPException(
            status_code=500, detail="Failed to generate registration token"
        )

    email_service = EmailService()
    await email_service.send_invitation_email(
        to_email=user_data.email, token=new_user.registration_token
    )

    return {"message": "Invitation sent", "email": user_data.email}


@router.post("/complete-registration", status_code=status.HTTP_201_CREATED)
async def complete_registration_endpoint(
    user: UserCompleteRegistrationSchema, db: Session = Depends(get_db)
) -> UserOutSchema:
    new_user = complete_registration(db, user)
    return UserOutSchema.model_validate(new_user)


@router.post("/login")
async def login_endpoint(
    user_data: UserLoginSchema, db: Session = Depends(get_db)
) -> dict:
    user = authenticate_user(db, user_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_database_token(user.id, db)
    return {"access_token": token.token, "token_type": "bearer"}


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_token: Token = Depends(get_current_token), db: Session = Depends(get_db)
):
    logout_user(db, current_token)
    logger.info("User logged out successfully")
    return


@router.post("/token")
async def login_oauth2(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> dict[str, str]:
    login_data = UserLoginSchema(
        username=form_data.username, password=form_data.password
    )

    user = authenticate_user(db, login_data)
    if not user:
        logger.warning(f"Failed login attempt for username: '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_obj = create_database_token(user.id, db=db)
    logger.info(f"User '{user.username}' logged in successfully")
    return {"access_token": token_obj.token, "token_type": "bearer"}
