from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID
import re

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: Annotated[str, EmailStr] = Field(
        description="User's email address (unique)",
        examples=["user@example.com"],
    )
    first_name: str = Field(
        description="User's first name",
        min_length=1,
        max_length=100,
        examples=["John"],
    )
    last_name: str = Field(
        description="User's last name",
        min_length=1,
        max_length=100,
        examples=["Doe"],
    )
    access: bool = Field(
        default=False,
        description="Flag indicating whether user has elevated access",
    )
    is_active: bool = Field(
        default=False,
        description="Flag indicating whether user account is active",
    )


class UserCreate(UserBase):
    password: str = Field(
        description="User's password",
        min_length=8,
        max_length=100,
        examples=["SomePassword1!"],
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("password must contain at least one special character")
        return value


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the user was soft-deleted"
    )


class UserSchemas(UserRead):
    """Backward compatible alias used across the services."""


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
