from core.exceptions.base_exception import BaseAppException


class AdminAvailabilityNotFoundException(BaseAppException):
    """Exception raised when an admin availability is not found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Admin availability not found",
            status_code=404,
            detail=detail or "The requested admin availability does not exist",
        )


class AdminAvailabilityAlreadyExistsException(BaseAppException):
    """Exception raised when trying to create an admin availability that already exists."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Admin availability already exists",
            status_code=400,
            detail=detail or "An availability for this admin and date already exists",
        )


class AdminAvailabilitiesNotFoundException(BaseAppException):
    """Exception raised when no admin availabilities are found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Admin availabilities not found",
            status_code=404,
            detail=detail or "No admin availabilities found matching the criteria",
        )


class InvalidAdminAvailabilityDataException(BaseAppException):
    """Exception raised when admin availability data is invalid."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Invalid admin availability data",
            status_code=400,
            detail=detail or "The provided admin availability data is invalid",
        )
