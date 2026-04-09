from datetime import date as DateType
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from enums import AppointmentStatus
from schemas.services_schema import ServiceRead


class AppointmentCreate(BaseModel):
    date: DateType
    services: list[UUID]


# TODO: Adicionar campo meio de pagamento (pix, cartão de crédito, dinheiro)
class AppointmentRead(BaseModel):
    id: UUID
    date: DateType
    status: AppointmentStatus

    client_id: UUID
    admin_id: Optional[UUID] = None

    services: List[ServiceRead]

    cancel_reason: Optional[str] = None
    cancelled_at: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime

    @field_validator("services", mode="before")
    @classmethod
    def extract_services(cls, value):
        if isinstance(value, list):
            return [
                item.service if hasattr(item, "service") else item
                for item in value
                if (hasattr(item, "service") and item.service is not None)
                or not hasattr(item, "service")
            ]
        return value

    class Config:
        from_attributes = True


class AppointmentCancel(BaseModel):
    cancel_reason: str


class AppointmentClientUpdate(BaseModel):
    date: Optional[DateType] = None
    services: Optional[list[UUID]] = None


class AppointmentAdminUpdate(BaseModel):
    status: AppointmentStatus
