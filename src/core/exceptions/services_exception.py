from core.exceptions.base_exception import BaseAppException


class ServiceNotFoundException(BaseAppException):
    """Exception raised when a service is not found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Service not found",
            status_code=404,
            detail=detail or "The requested service does not exist",
        )


class ServiceAlreadyExistsException(BaseAppException):
    """Exception raised when trying to create a service that already exists."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Service already exists",
            status_code=400,
            detail=detail or "A service with this name already exists",
        )


class ServicesNotFoundException(BaseAppException):
    """Exception raised when no services are found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Services not found",
            status_code=404,
            detail=detail or "No services found matching the criteria",
        )


class InvalidServiceDataException(BaseAppException):
    """Exception raised when service data is invalid."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Invalid service data",
            status_code=400,
            detail=detail or "The provided service data is invalid",
        )
