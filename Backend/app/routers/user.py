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
    RequestPasswordResetSchema,
    ResetPasswordSchema,
    ChangeRoleSchema,
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
    request_password_reset,
    reset_password,
    change_user_role,
    search_users,
)

router = APIRouter(tags=["users"], prefix="/users")

require_admin = RoleChecker([RoleType.ADMIN])


@router.get("/", response_model=list[UserOutSchema], status_code=status.HTTP_200_OK)
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Max number of records to return"),
    include_inactive: bool = Query(False, description="Include inactive users"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    users = get_users(db, skip=skip, limit=limit, include_inactive=include_inactive)
    logger.info(
        f"Admin {current_user.username} listed {len(users)} users "
        f"(skip={skip}, limit={limit}, include_inactive={include_inactive})"
    )
    return users


@router.get("/{user_id}", response_model=UserOutSchema, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    include_inactive: bool = Query(False, description="Include inactive users"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = get_user_by_id(db, user_id=user_id, include_inactive=include_inactive)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    logger.info(
        f"Admin {current_user.username} retrieved user {user.username} "
        f"(include_inactive={include_inactive})"
    )
    return user


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


@router.put("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = deactivate_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or already inactive",
        )
    logger.info(f"User {user_id} deactivated")


@router.put("/{user_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = activate_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or already active",
        )
    logger.info(f"User {user_id} activated")


@router.put(
    "/{user_id}/update",
    response_model=UserWithEmployeeOutSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user_endpoint(
    user_id: int,
    update_data: EmployeeUpdateSchema,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    user = update_user(db, user_id=user_id, update_data=update_data)
    logger.info(f"Updated employee: {user.username}")
    return UserWithEmployeeOutSchema.from_user(user)


@router.put("/{user_id}/change-password", status_code=status.HTTP_200_OK)
async def change_password_endpoint(
    user_id: int,
    data: ChangePasswordSchema,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    success = change_password(
        db,
        user_id=user_id,
        old_password=data.old_password,
        new_password=data.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid old password or user not found",
        )

    logger.info(f"Password changed for user {user_id}")
    return {"detail": "Password updated successfully"}


@router.put("/request-reset-password", status_code=status.HTTP_200_OK)
async def request_password_reset_endpoint(
    data: RequestPasswordResetSchema,
    db: Session = Depends(get_db),
):
    success = request_password_reset(db, email=data.email)

    if not success:
        logger.info(f"No user with email {data.email} found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User email not found",
        )

    logger.info(f"Password reset requested for {data.email}")

    return {"detail": "Password reset requested. Please check your email."}


@router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password_endpoint(
    data: ResetPasswordSchema,
    db: Session = Depends(get_db),
):
    success = reset_password(db, token=data.token, new_password=data.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    logger.info(f"Password reset for user with token {data.token}")
    return {"detail": "Password has been reset successfully"}


@router.put("/{user_id}/change_user_role", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_role_endpoints(
    user_id: int,
    data: ChangeRoleSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    success = change_user_role(db, user_id=user_id, new_role=data.role)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or employee not found",
        )
    logger.info(f"Role of user {user_id} changed to {data.role}")


@router.get(
    "/search",
    response_model=List[UserWithEmployeeOutSchema],
    status_code=status.HTTP_200_OK,
)
async def search_users_endpoint(
    q: str | None = None,
    role: RoleType | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
):
    users = search_users(db, query=q, role=role, is_active=is_active)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
        )

    logger.info(f"Found {len(users)} user(s) for query='{q}'")

    return [UserWithEmployeeOutSchema.from_user(user) for user in users]
