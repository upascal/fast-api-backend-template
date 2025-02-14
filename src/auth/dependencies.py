from datetime import datetime
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.exceptions import (
    AuthTokenExpiredException,
    AuthTokenInvalidException,
    UserNotFoundException
)
from src.db.base import get_db
from src.users import service as users_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    """Dependency to get current authenticated user from JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("user_id")
        if not user_id:
            raise AuthTokenInvalidException()
            
        # Check token expiration
        exp = payload.get("exp")
        if not exp or datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise AuthTokenExpiredException()
            
    except JWTError:
        raise AuthTokenInvalidException()

    user = await users_service.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundException()

    if not user["is_active"]:
        raise AuthTokenInvalidException(detail="Inactive user")

    return user


async def get_current_active_superuser(
    current_user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    """Dependency to get current authenticated superuser."""
    if not current_user["is_superuser"]:
        raise AuthTokenInvalidException(detail="Not enough permissions")
    return current_user
