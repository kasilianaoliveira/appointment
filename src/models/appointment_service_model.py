from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base

if TYPE_CHECKING:
    from models.appointment_model import AppointmentModel
    from models.service_model import ServiceModel


class AppointmentServiceModel(Base):
    __tablename__ = "appointment_services"

    appointment_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("appointments.id"),
        primary_key=True,
    )

    service_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("services.id"),
        primary_key=True,
    )

    appointment: Mapped["AppointmentModel"] = relationship(
        back_populates="services",
    )

    service: Mapped["ServiceModel"] = relationship(
        back_populates="appointments",
    )
