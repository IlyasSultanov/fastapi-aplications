"""
JWT and password utilities.

Adds `iss`, `aud`, `iat`, `exp` fields to tokens, validates them on decode,
and provides bcrypt helpers for secure password handling.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import bcrypt
import jwt as pyjwt
from app.core.config import settings


def encode_jwt(
    payload: Dict[str, Any],
    private_key: str = settings.private_key.read_text(),
    algorithm: str = settings.algorithm,
    expires_in: int = settings.access_token_expires_minutes,
    expires_timedelta: Optional[timedelta] = None,
    issuer: str = settings.issuer,
    audience: str = settings.audience,
) -> str:
    """
    Encode a JWT with the provided payload and options.

    Args:
        payload: Claims to include in the token.
        private_key: Private key for signing.
        algorithm: Signing algorithm (RS256 by default).
        expires_in: Expiration time in minutes.
        expires_timedelta: Alternative expiration delta overriding expires_in.
        issuer: Token issuer value.
        audience: Token audience value.

    Returns:
        str: Signed JWT string.
    """
    now = datetime.utcnow()
    exp = now + (expires_timedelta or timedelta(minutes=expires_in))
    to_encode = {**payload, "iss": issuer, "aud": audience, "exp": exp, "iat": now}

    token = pyjwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return token


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.public_key.read_text(),
    algorithm: str = settings.algorithm,
    issuer: str = settings.issuer,
    audience: str = settings.audience,
) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.

    Args:
        token: Encoded JWT to decode.
        public_key: Public key used for signature verification.
        algorithm: Expected signing algorithm.
        issuer: Expected issuer.
        audience: Expected audience.

    Returns:
        Dict[str, Any]: Decoded claim set.

    Raises:
        InvalidTokenError: If validation fails.
    """
    decoded = pyjwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
        audience=audience,
        issuer=issuer,
    )
    return decoded


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password.

    Returns:
        str: UTF-8 encoded bcrypt hash.
    """
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode(), salt)
    return hashed_bytes.decode("utf-8")


def validate_password(password: str, hash_pass: str) -> bool:
    """
    Validate a password against a stored bcrypt hash.

    Args:
        password: Plain text password.
        hash_pass: Stored bcrypt hash (as UTF-8 string).

    Returns:
        bool: True if the password matches, otherwise False.
    """
    return bcrypt.checkpw(password.encode(), hash_pass.encode())
