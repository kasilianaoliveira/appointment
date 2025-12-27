from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base
from enums import UserRole
from sqlalchemy import Enum
if TYPE_CHECKING:
    from models.admin_daily_limit_model import AdminDailyLimitModel
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
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    admin_daily_limits: Mapped[List["AdminDailyLimitModel"]] = relationship(
        back_populates="admin",
    )
    
    client_appointments: Mapped[List["AppointmentModel"]] = relationship(
        back_populates="client",
        foreign_keys="AppointmentModel.client_id",
    )
    
    admin_appointments: Mapped[List["AppointmentModel"]] = relationship(
        back_populates="admin",
        foreign_keys="AppointmentModel.admin_id",
    )
    
    
    