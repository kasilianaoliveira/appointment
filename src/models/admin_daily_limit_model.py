from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from enums import WeekDay
from sqlalchemy import Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base

if TYPE_CHECKING:
    from models.user_model import UserModel


class AdminDailyLimitModel(Base):
    __tablename__ = "admin_daily_limits"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    admin_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    week_day: Mapped[WeekDay] = mapped_column(
        Enum(WeekDay, name="week_day"), nullable=False
    )
    limit: Mapped[int] = mapped_column(Integer, nullable=False)

    admin: Mapped["UserModel"] = relationship(
        foreign_keys=[admin_id],
        back_populates="admin_daily_limits",
    )

    __table_args__ = (
        UniqueConstraint("admin_id", "week_day", name="uq_admin_week_day"),
    )
