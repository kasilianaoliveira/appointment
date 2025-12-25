from core.exceptions.base_exception import BaseAppException


class UserNotFoundException(BaseAppException):
    """Exception raised when a user is not found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="User not found",
            status_code=404,
            detail=detail or "The requested user does not exist",
        )


class UserAlreadyExistsException(BaseAppException):
    """Exception raised when trying to create a user that already exists."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="User already exists",
            status_code=400,
            detail=detail or "A user with this email already exists",
        )


class UsersNotFoundException(BaseAppException):
    """Exception raised when no users are found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Users not found",
            status_code=404,
            detail=detail or "No users found matching the criteria",
        )


class InvalidUserDataException(BaseAppException):
    """Exception raised when user data is invalid."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Invalid user data",
            status_code=400,
            detail=detail or "The provided user data is invalid",
        )
