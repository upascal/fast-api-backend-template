from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_active_superuser, get_current_user
from src.core.schemas import ResponseModel
from src.db.base import get_db
from src.users import service
from src.users.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=ResponseModel[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Create new user."""
    user = await service.create(db, user_data)
    return {
        "success": True,
        "message": "User created successfully",
        "data": user
    }


@router.get(
    "",
    response_model=ResponseModel[list[UserResponse]],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> dict:
    """Get all users. Only for superusers."""
    users = await service.get_multi(db, skip=skip, limit=limit)
    return {
        "success": True,
        "data": users
    }


@router.get("/{user_id}", response_model=ResponseModel[UserResponse])
async def get_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    """Get user by ID."""
    # Only allow users to get their own data unless they're superusers
    if current_user["id"] != user_id and not current_user["is_superuser"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = await service.get_by_id(db, user_id)
    return {
        "success": True,
        "data": user
    }


@router.put("/{user_id}", response_model=ResponseModel[UserResponse])
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    """Update user."""
    # Only allow users to update their own data unless they're superusers
    if current_user["id"] != user_id and not current_user["is_superuser"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = await service.update(db, user_id, user_data)
    return {
        "success": True,
        "message": "User updated successfully",
        "data": user
    }


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> None:
    """Delete user."""
    # Only allow users to delete their own account unless they're superusers
    if current_user["id"] != user_id and not current_user["is_superuser"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    await service.delete(db, user_id)
