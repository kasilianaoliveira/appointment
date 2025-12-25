from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base

if TYPE_CHECKING:
    from models.user_model import UserModel


class AdminAvailabilityModel(Base):
    __tablename__ = "admin_availability"

    __table_args__ = (
        UniqueConstraint("admin_id", "available_date", name="uq_admin_date"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    admin_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    available_date: Mapped[date] = mapped_column(Date, nullable=False)
    max_appointments: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    admin: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="availabilities",
    )
