from datetime import timedelta
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import create_access_token, verify_password
from src.core.config import settings
from src.core.exceptions import AuthFailedException
from src.users import service as users_service


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
) -> dict[str, Any]:
    """Authenticate user with email and password."""
    user = await users_service.get_by_email(db, email)
    
    if not user:
        raise AuthFailedException()
    
    if not verify_password(password, user["hashed_password"]):
        raise AuthFailedException()
    
    if not user["is_active"]:
        raise AuthFailedException(detail="Inactive user")
    
    return user


async def login(
    db: AsyncSession,
    email: str,
    password: str
) -> dict[str, str]:
    """Login user and return access token."""
    user = await authenticate_user(db, email, password)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user["id"])},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
