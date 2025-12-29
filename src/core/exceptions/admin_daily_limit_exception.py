from core.exceptions.base_exception import BaseAppException


class AdminDailyLimitNotFoundException(BaseAppException):
    """Exception raised when an admin daily limit is not found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Admin daily limit not found",
            status_code=404,
            detail=detail or "The requested admin daily limit does not exist",
        )


class AdminDailyLimitAlreadyExistsException(BaseAppException):
    """Exception raised when trying to create an admin daily limit that already exists."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Admin daily limit already exists",
            status_code=400,
            detail=detail or "An admin daily limit with these details already exists",
        )
