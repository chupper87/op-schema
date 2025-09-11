from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Query

from ..models import User
from ..core.enums import RoleType
from ..core.db_setup import get_db
from ..core.security import RoleChecker
from ..core.logger import logger
from ..schemas.user import (
    UserOutSchema,
    UserWithEmployeeOutSchema,
    ChangePasswordSchema,
)
from ..schemas.employee import EmployeeUpdateSchema
from ..crud.user import (
    delete_user,
    deactivate_user,
    activate_user,
    get_users,
    get_user_by_id,
    update_user,
    change_password,
)

router = APIRouter(tags=["users"], prefix="/users")

require_admin = RoleChecker([RoleType.ADMIN])


@router.get("/", response_model=List[UserOutSchema], status_code=status.HTTP_200_OK)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = Query(False, description="Include inactive users"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> List[UserOutSchema]:
    users = get_users(db, skip=skip, limit=limit, include_inactive=include_inactive)
    logger.info(
        f"Admin {current_user.username} listed {len(users)} users (include_inactive={include_inactive})"
    )
    return [UserOutSchema.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserOutSchema, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
    include_inactive: bool = Query(False, description="Include inactive users"),
) -> UserOutSchema:
    user = get_user_by_id(db, user_id=user_id, include_inactive=include_inactive)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    logger.info(f"Admin {current_user.username} retrieved user {user.username}")
    return UserOutSchema.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    logger.info(f"Admin {current_user.username} is deleting user {user_id}")

    success = delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    logger.info(f"User {user_id} deleted successfully by admin {current_user.username}")


@router.put("/{user_id}/deactivate", status_code=status.HTTP_200_OK)
async def deactivate_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    result = deactivate_user(db, user_id=user_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_id} is already inactive",
        )

    logger.info(f"User {user_id} deactivated by admin {current_user.username}")
    return {"detail": f"User {user_id} deactivated successfully"}


@router.put("/{user_id}/activate", status_code=status.HTTP_200_OK)
async def activate_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    result = activate_user(db, user_id=user_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_id} is already active",
        )

    logger.info(f"User {user_id} activated by admin {current_user.username}")
    return {"detail": f"User {user_id} activated successfully"}


@router.put(
    "/{user_id}/update",
    response_model=UserWithEmployeeOutSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user_endpoint(
    user_id: int,
    update_data: EmployeeUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = update_user(db, user_id=user_id, update_data=update_data)
    logger.info(f"Updated employee: {user.username}")
    return UserWithEmployeeOutSchema.from_user(user)


@router.put(
    "/{user_id}/change-password",
    response_model=ChangePasswordSchema,
    status_code=status.HTTP_200_OK,
)
async def change_password_endpoint(
    db: Session, user_id: int, old_password: str, new_password: str
):
    success = change_password(
        db, user_id=user_id, old_password=old_password, new_password=new_password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid old password or user not found",
        )
    logger.info("Password has been changed for user {user_id}")

    return {"detail": "Password updated successfully"}
