from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base
from enums import UserRole

if TYPE_CHECKING:
    from models.admin_availability_model import AdminAvailabilityModel
    from models.appointment_model import AppointmentModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    role: Mapped[UserRole] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    client_appointments: Mapped[list["AppointmentModel"]] = relationship(
        "AppointmentModel",
        foreign_keys="AppointmentModel.client_id",
        back_populates="client",
    )

    admin_appointments: Mapped[list["AppointmentModel"]] = relationship(
        "AppointmentModel",
        foreign_keys="AppointmentModel.admin_id",
        back_populates="admin",
    )

    availabilities: Mapped[list["AdminAvailabilityModel"]] = relationship(
        "AdminAvailabilityModel",
        back_populates="admin",
    )
