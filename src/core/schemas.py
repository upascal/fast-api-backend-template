from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar('T')


class CustomModel(BaseModel):
    """Base model with custom configurations."""
    
    model_config = ConfigDict(
        from_attributes=True,  # Allow ORM model parsing
        populate_by_name=True,  # Allow population by field name as well as alias
        use_enum_values=True,  # Use enum values rather than enum objects
        json_encoders={
            datetime: lambda dt: dt.isoformat(),
        }
    )


class ResponseModel(CustomModel, Generic[T]):
    """Base model for standard responses."""
    
    success: bool = True
    message: str | None = None
    data: T | None = None


class PaginatedResponse(ResponseModel[T]):
    """Base model for paginated responses."""
    
    total: int
    page: int
    size: int
    pages: int
