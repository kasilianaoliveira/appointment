from core.exceptions.base_exception import BaseAppException


class AppointmentNotFoundException(BaseAppException):
    """Exception raised when an appointment is not found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Appointment not found",
            status_code=404,
            detail=detail or "The requested appointment does not exist",
        )


class AppointmentAlreadyExistsException(BaseAppException):
    """Exception raised when trying to create an appointment that already exists."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Appointment already exists",
            status_code=400,
            detail=detail or "An appointment with these details already exists",
        )


class AppointmentsNotFoundException(BaseAppException):
    """Exception raised when no appointments are found."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Appointments not found",
            status_code=404,
            detail=detail or "No appointments found matching the criteria",
        )


class InvalidAppointmentDataException(BaseAppException):
    """Exception raised when appointment data is invalid."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Invalid appointment data",
            status_code=400,
            detail=detail or "The provided appointment data is invalid",
        )


class AppointmentAlreadyAcceptedException(BaseAppException):
    """Exception raised when trying to accept an appointment that is already accepted."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Appointment already accepted",
            status_code=400,
            detail=detail or "This appointment has already been accepted by an admin",
        )


class AdminNotAvailableException(BaseAppException):
    """Exception raised when admin has reached max appointments for a date."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Admin not available",
            status_code=400,
            detail=detail
            or "The admin has reached the maximum number of appointments for this date",
        )


class InvalidAppointmentStateException(BaseAppException):
    """Exception raised when appointment state is invalid."""

    def __init__(self, detail: str | None = None):
        super().__init__(
            message="Invalid appointment state",
            status_code=400,
            detail=detail or "The appointment state is invalid",
        )
