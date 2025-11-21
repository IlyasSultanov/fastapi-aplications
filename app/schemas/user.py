from pydantic import EmailStr, ValidationError, field_validator, Field
from . import BaseModels


class UserSchemas(BaseModels):
    email: EmailStr = Field(
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
    password: str = Field(
        description="User's password",
        min_length=8,
        max_length=100,
        examples=["Some password"],
    )

    @field_validator("email")
    @classmethod
    async def validate_email(cls, email: EmailStr):
        if email is None:
            raise ValidationError("Email cannot be None")
        return email

    @field_validator("password")
    @classmethod
    async def validate_password(cls, value: str):
        if value is None:
            raise ValidationError("Password cannot be None")
        return value
