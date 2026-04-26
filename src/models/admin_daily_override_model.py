from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID,
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
from models.constants import USER_ID_FOREIGN_KEY

if TYPE_CHECKING:
    from models.user_model import UserModel


class AdminDailyOverrideModel(Base):
    __tablename__ = "admin_daily_override"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    admin_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(USER_ID_FOREIGN_KEY),
        nullable=False,
        index=True,
    )
    date_modified: Mapped[date] = mapped_column(
        Date, nullable=False, index=True
    )
    limit: Mapped[int] = mapped_column(Integer, nullable=False)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )

    admin: Mapped["UserModel"] = relationship(
        back_populates="admin_daily_override"
    )

    __table_args__ = (
        UniqueConstraint("admin_id", "date_modified", name="uq_admin_date"),
    )
