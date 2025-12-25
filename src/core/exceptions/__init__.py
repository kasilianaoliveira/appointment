"""Custom exceptions for the application."""

from core.exceptions.base_exception import BaseAppException
from core.exceptions.services_exception import (
    InvalidServiceDataException,
    ServiceAlreadyExistsException,
    ServiceNotFoundException,
    ServicesNotFoundException,
)
from core.exceptions.user_exception import (
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
    "ServiceNotFoundException",
    "ServiceAlreadyExistsException",
    "ServicesNotFoundException",
    "InvalidServiceDataException",
]
