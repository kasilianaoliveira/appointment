from __future__ import annotations

from datetime import date as DateType
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base
from enums import AppointmentStatus
from enums.payments_method import PaymentsMethod
from models.constants import USER_ID_FOREIGN_KEY

if TYPE_CHECKING:
    from models.appointment_service_model import AppointmentServiceModel
    from models.user_model import UserModel


class AppointmentModel(Base):
    __tablename__ = "appointments"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    date: Mapped[DateType] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(
            AppointmentStatus,
            name="appointment_status",
            values_callable=lambda x: [e.value for e in AppointmentStatus],
        ),
        nullable=False,
        server_default=AppointmentStatus.PENDING.value,
    )

    cancel_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    refused_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    reschedule_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    payments_method: Mapped[PaymentsMethod] = mapped_column(
        Enum(
            PaymentsMethod,
            name="payments_method",
            values_callable=lambda values: [value.value for value in values],
        ),
        nullable=False,
        default=PaymentsMethod.CASH,
        server_default=PaymentsMethod.CASH.value,
    )

    proposed_date: Mapped[DateType | None] = mapped_column(
        Date,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    refused_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    reschedule_requested_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    client_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(USER_ID_FOREIGN_KEY),
        nullable=False,
        index=True,
    )
    admin_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(USER_ID_FOREIGN_KEY),
        nullable=True,
        index=True,
    )
    created_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(USER_ID_FOREIGN_KEY),
        nullable=True,
        index=True,
    )
    accepted_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(USER_ID_FOREIGN_KEY),
        nullable=True,
        index=True,
    )
    refused_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(USER_ID_FOREIGN_KEY),
        nullable=True,
        index=True,
    )
    cancelled_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(USER_ID_FOREIGN_KEY),
        nullable=True,
        index=True,
    )
    reschedule_requested_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(USER_ID_FOREIGN_KEY),
        nullable=True,
        index=True,
    )

    client: Mapped["UserModel"] = relationship(
        foreign_keys=[client_id],
        back_populates="client_appointments",
    )
    admin: Mapped["UserModel"] = relationship(
        foreign_keys=[admin_id],
        back_populates="admin_appointments",
    )
    created_by_user: Mapped["UserModel | None"] = relationship(
        foreign_keys=[created_by],
    )
    accepted_by_user: Mapped["UserModel | None"] = relationship(
        foreign_keys=[accepted_by],
    )
    refused_by_user: Mapped["UserModel | None"] = relationship(
        foreign_keys=[refused_by],
    )
    cancelled_by_user: Mapped["UserModel | None"] = relationship(
        foreign_keys=[cancelled_by],
    )
    reschedule_requested_by_user: Mapped["UserModel | None"] = relationship(
        foreign_keys=[reschedule_requested_by],
    )

    services: Mapped[list["AppointmentServiceModel"]] = relationship(
        back_populates="appointment",
        cascade="all, delete-orphan",
    )
