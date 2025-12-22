"""Custom exceptions for the application."""

from core.exceptions.base_exception import BaseAppException
from core.exceptions.user_expection import (
    InvalidUserDataException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UsersNotFoundException,
)

__all__ = [
    "BaseAppException",
    "UserNotFoundException",
    "UserAlreadyExistsException",
    "UsersNotFoundException",
    "InvalidUserDataException",
]
