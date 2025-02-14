from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_password_hash
from src.core.exceptions import UserAlreadyExistsException, UserNotFoundException
from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate


async def get_by_id(db: AsyncSession, user_id: UUID) -> dict[str, Any] | None:
    """Get user by ID."""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        return None
        
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


async def get_by_email(db: AsyncSession, email: str) -> dict[str, Any] | None:
    """Get user by email."""
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        return None
        
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "hashed_password": user.hashed_password,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


async def create(db: AsyncSession, user_data: UserCreate) -> dict[str, Any]:
    """Create new user."""
    # Check if user with this email already exists
    if await get_by_email(db, user_data.email):
        raise UserAlreadyExistsException()
    
    # Create new user
    db_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_active=user_data.is_active,
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return await get_by_id(db, db_user.id)


async def update(
    db: AsyncSession,
    user_id: UUID,
    user_data: UserUpdate
) -> dict[str, Any]:
    """Update user."""
    # Get existing user
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise UserNotFoundException()
    
    # Update user fields
    update_data = user_data.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return await get_by_id(db, user.id)


async def get_multi(
    db: AsyncSession,
    *,
    skip: int = 0,
    limit: int = 100
) -> list[dict[str, Any]]:
    """Get multiple users with pagination."""
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return [
        {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        for user in users
    ]


async def delete(db: AsyncSession, user_id: UUID) -> None:
    """Delete user."""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise UserNotFoundException()
    
    await db.delete(user)
    await db.commit()
