from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import service
from src.auth.dependencies import get_current_user
from src.core.schemas import ResponseModel
from src.db.base import get_db
from src.users.schemas import Token, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    """Login user and return access token."""
    token = await service.login(
        db=db,
        email=form_data.username,  # OAuth2 form uses username field for email
        password=form_data.password,
    )
    return token


@router.get("/me", response_model=ResponseModel[UserResponse])
async def read_users_me(
    current_user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    """Get current authenticated user."""
    return {
        "success": True,
        "data": current_user
    }
