"""Custom exceptions for the application."""

from core.exceptions.admin_availability_exception import (
    AdminAvailabilitiesNotFoundException,
    AdminAvailabilityAlreadyExistsException,
    AdminAvailabilityNotFoundException,
    InvalidAdminAvailabilityDataException,
)
from core.exceptions.appointment_exception import (
    AdminNotAvailableException,
    AppointmentAlreadyAcceptedException,
    AppointmentAlreadyExistsException,
    AppointmentNotFoundException,
    AppointmentsNotFoundException,
    InvalidAppointmentDataException,
)
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
    "AppointmentNotFoundException",
    "AppointmentAlreadyExistsException",
    "AppointmentsNotFoundException",
    "InvalidAppointmentDataException",
    "AppointmentAlreadyAcceptedException",
    "AdminNotAvailableException",
    "AdminAvailabilityNotFoundException",
    "AdminAvailabilityAlreadyExistsException",
    "AdminAvailabilitiesNotFoundException",
    "InvalidAdminAvailabilityDataException",
]
