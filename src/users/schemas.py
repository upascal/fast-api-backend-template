from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field

from src.core.schemas import CustomModel


class UserBase(CustomModel):
    """Base schema for user data."""
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=64)


class UserUpdate(CustomModel):
    """Schema for updating a user."""
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = Field(None, min_length=8, max_length=64)


class UserInDB(UserBase):
    """Schema for user data from database."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_superuser: bool = False


class UserResponse(UserInDB):
    """Schema for user response."""
    pass


# Auth schemas
class Token(CustomModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"


class TokenData(CustomModel):
    """Schema for token payload."""
    user_id: UUID
    exp: datetime
