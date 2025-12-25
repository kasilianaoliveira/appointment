from enum import StrEnum


class AppointmentStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
