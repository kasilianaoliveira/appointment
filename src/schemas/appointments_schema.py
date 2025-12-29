from datetime import date as DateType, datetime
from typing import List, Optional
from uuid import UUID
from enums import AppointmentStatus
from pydantic import BaseModel, model_validator
from schemas import ServiceRead


class AppointmentCreate(BaseModel):
    date: DateType
    services: list[UUID]


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

    @model_validator(mode="before")
    @classmethod
    def extract_services(cls, data):
        if hasattr(data, "services"):

            result = {
                key: getattr(data, key)
                for key in cls.model_fields.keys()
                if key != "services"
            }
            services = [
                item.service
                for item in data.services
                if hasattr(item, "service") and item.service is not None
            ]
            result["services"] = services
            return result
        return data

    class Config:
        from_attributes = True


class AppointmentCancel(BaseModel):
    cancel_reason: str


class AppointmentClientUpdate(BaseModel):
    date: Optional[DateType] = None
    services: Optional[list[UUID]] = None


class AppointmentAdminUpdate(BaseModel):
    status: AppointmentStatus
