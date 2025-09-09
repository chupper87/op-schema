from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..models import User
from ..core.enums import RoleType
from ..core.db_setup import get_db
from ..core.security import RoleChecker, create_database_token, get_current_superuser
from ..core.logger import logger
from ..schemas.user import (
    UserCompleteRegistrationSchema,
    UserOutSchema,
    UserInviteSchema,
    UserLoginSchema,
)
from ..crud.user import complete_registration, authenticate_user

router = APIRouter(tags=["user"], prefix="/user")

require_admin = RoleChecker([RoleType.ADMIN])


@router.post("/invite", status_code=status.HTTP_201_CREATED)
async def invite_user_endpoint(
    user_data: UserInviteSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    pass
    # new_user = invite_user(db, user_data)

    # # Skicka email med registration_token här
    # # send_invitation_email(user_data.email, new_user.registration_token)

    # return {"message": "Invitation sent", "email": user_data.email}


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
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    try:
        db.delete(user)
        db.commit()
        logger.success(f"User {user.username} (id={user.id}) hard deleted successfully")
    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to hard delete user {user_id}: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the user"
        )


# # Dactivate and reactivate user
# @router.put("/{user_id}/deactivate", status_code=status.HTTP_200_OK)
# async def deactivate_user(
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin),
# ):
#     user = db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

#     if not user.is_active:
#         raise HTTPException(
#             status_code=409, detail=f"User {user_id} is already inactive"
#         )

#     user.is_active = False
#     if user.employee:
#         user.employee.is_active = False

#     db.commit()
#     logger.info(f"User {user.username} (id={user.id}) deactivated")
#     return {"detail": f"User {user.username} deactivated"}


# @router.put("/{user_id}/activate", status_code=status.HTTP_200_OK)
# async def activate_user(
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin),
# ):
#     user = db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

#     if user.is_active:
#         raise HTTPException(status_code=409, detail=f"User {user_id} is already active")

#     user.is_active = True
#     if user.employee:
#         user.employee.is_active = True

#     db.commit()
#     logger.info(f"User {user.username} (id={user.id}) activated")
#     return {"detail": f"User {user.username} activated"}


# # List users
# @router.get("/", response_model=List[UserOutSchema], status_code=status.HTTP_200_OK)
# async def list_users(
#     skip: int = 0,
#     limit: int = 100,
#     include_inactive: bool = Query(False, description="Include inactive users"),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin),
# ) -> List[UserOutSchema]:
#     query = select(User).offset(skip).limit(limit)

#     if not include_inactive:
#         query = query.where(User.is_active == True)  # noqa: E712

#     users = db.scalars(query).all()
#     logger.info(
#         f"Admin {current_user.username} listed {len(users)} users (include_inactive={include_inactive})"
#     )
#     return users  # type: ignore


# @router.get("/{user_id}", response_model=UserOutSchema, status_code=status.HTTP_200_OK)
# async def get_user(
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin),
#     include_inactive: bool = Query(False, description="Include inactive users"),
# ) -> UserOutSchema:
#     user = db.get(User, user_id)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with ID {user_id} not found",
#         )

#     if not include_inactive and not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with ID {user_id} is inactive",
#         )

#     logger.info(f"{current_user.username} listed {user}")

#     return UserOutSchema.model_validate(user)
