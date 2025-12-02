"""
Module providing authentication services, functions
for user management and JWT handling.
"""

# Python imports
from typing import Dict, Any
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# JWT imports
from jwt.exceptions import InvalidTokenError

# SQLAlchemy imports
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# project helpers
from app.database.db import get_db
from app.auth import utils as auth_utils
from app.auth.utils import hash_password

# import models
from app.models.user import User

# import schemas
from app.schemas.access_token import AccessTokenRequest
from app.schemas.user import UserSchemas, UserCreate, UserRead

http_bearer = HTTPBearer()


async def is_jti_in_denylist(jti: str) -> bool:
    """
    Placeholder denylist check. Replace with persistent storage lookup if needed.
    """
    return False


async def create_user(db: AsyncSession, user: UserCreate) -> Dict[str, Any]:
    """
    Create a new user in the database.

    Args:
        db: Database session
        user: Data for user creation

    Returns:
        Dict[str, Any]: Operation result with user data or error details

    Raises:
        IntegrityError: When attempting to create a user with an existing username/email
    """
    hashed_password = hash_password(user.password)

    user_obj = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
        is_active=True,
        access=True,
    )

    db.add(user_obj)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        return {
            "status": "error",
            "message": "User with this email already exists",
            "context": {"detail": str(exc.orig) if exc.orig else None},
        }
    await db.refresh(user_obj)
    # Do not include hashed_password in the response
    user_read = UserRead.model_validate(user_obj)
    return {
        "status": "ok",
        "user": user_read,
    }


async def _get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Return a user by username or None if not found.

    Does not mutate the database. Used to eliminate code duplication.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def validate_auth_user(
    access_token: AccessTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> UserSchemas:
    """Validate user credentials.

    - Find a user by username in the database
    - Compare the password against the bcrypt hash
    - Ensure the user is active

    Returns `UserSchema` without changing endpoint external behavior.
    """
    user: User | None = await _get_user_by_email(db, access_token.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    if not auth_utils.validate_password(access_token.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user.email} has not been activated",
        )

    return UserSchemas(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        deleted_at=user.deleted_at,
    )


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> Dict[str, Any]:
    """
    Extract and decode a JWT token from the Authorization header.

    Args:
        credentials: Bearer token from the Authorization header

    Returns:
        dict: Decoded JWT token payload

    Raises:
        AuthException: For an incorrect or invalid token
    """
    try:
        token = credentials.credentials
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db),
) -> UserSchemas:
    """Return the current user specified in payload.sub.

    If the user is not found or `sub` is missing — return 401.
    """
    jti = payload.get("jti")
    if jti and await is_jti_in_denylist(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )
    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    # Look up the user by ID
    result = await db.execute(select(User).where(User.id == user_uuid))
    user: User | None = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    return UserSchemas(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        deleted_at=user.deleted_at,
        access=user.access,
    )


async def get_current_active_user(
    user: UserSchemas = Depends(get_current_auth_user),
) -> UserSchemas:
    """Ensure the current user is active.

    Otherwise return 403.
    """
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not active.",
    )
