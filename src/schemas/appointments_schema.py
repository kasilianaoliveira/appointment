from datetime import date, datetime
from typing import List
from uuid import UUID

from enums import AppointmentStatus
from pydantic import BaseModel
from schemas import ServiceRead


class AppointmentCreate(BaseModel):
    date: date
    services: list[UUID]


class AppointmentRead(BaseModel):
    id: UUID
    date: date
    status: AppointmentStatus

    client_id: UUID
    admin_id: UUID | None = None

    services: List[ServiceRead]

    cancel_reason: str | None = None
    cancelled_at: datetime | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AppointmentCancel(BaseModel):
    cancel_reason: str


class AppointmentClientUpdate(BaseModel):
    date: date | None = None
    services: list[UUID] | None = None


class AppointmentAdminUpdate(BaseModel):
    status: AppointmentStatus
