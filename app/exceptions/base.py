from typing import Any, Optional, Dict


class ExceptionBase(Exception):
    """Base Exception"""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.message = message
        self.context = context or {}
        super().__init__(message)


class AuthException(ExceptionBase):
    """Auth Exception"""

    def __init__(
        self, message: str = "Access denied", context: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(f"Unauthorized: {message}", context)


class NotFoundException(ExceptionBase):
    """Not Found Exception"""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(f"Not Found: {message}", context)


class ValidationException(ExceptionBase):
    """Validation Exception"""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(f"Validation Error: {message}", context)


class ForbiddenException(ExceptionBase):

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(f"ForbiddenException: {message}", context)


class BadRequestException(ExceptionBase):

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(f"Bad Request: {message}", context)
