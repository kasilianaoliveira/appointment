from datetime import UTC, datetime
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from enums import AppointmentStatus
from enums.date_filter import FutureDateFilter
from models import AppointmentModel
from models.appointment_service_model import AppointmentServiceModel
from repositories.interfaces.appointments_interface import (
    IAppointmentRepository,
)
from utils import FUTURE_DATE_FILTERS


class AppointmentsRepository(IAppointmentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, appointment: AppointmentModel) -> AppointmentModel:
        self.session.add(appointment)
        await self.session.flush()

        appointment_id = appointment.id
        await self.session.commit()

        self.session.expunge(appointment)
        loaded_appointment = await self.get_by_id(appointment_id)
        if not loaded_appointment:
            raise ValueError(
                f"Failed to reload appointment {appointment_id} after save"
            )
        return loaded_appointment

    async def update(self, appointment: AppointmentModel) -> AppointmentModel:
        self.session.add(appointment)
        await self.session.commit()

        appointment_id = appointment.id
        self.session.expunge(appointment)
        loaded_appointment = await self.get_by_id(appointment_id)
        if not loaded_appointment:
            raise ValueError(
                f"Failed to reload appointment {appointment_id} after update"
            )
        return loaded_appointment

    async def delete(self, appointment: AppointmentModel) -> None:
        await self.session.delete(appointment)
        await self.session.commit()

    async def get_by_id(self, id: UUID) -> AppointmentModel | None:
        result = await self.session.execute(
            select(AppointmentModel)
            .options(
                selectinload(AppointmentModel.services).selectinload(
                    AppointmentServiceModel.service
                )
            )
            .where(AppointmentModel.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        params: Params,
        client_id: UUID | None = None,
        admin_id: UUID | None = None,
        status: AppointmentStatus | None = None,
        date_filter: FutureDateFilter | None = None,
    ) -> Page[AppointmentModel]:
        stmt = (
            select(AppointmentModel)
            .options(
                selectinload(AppointmentModel.services).selectinload(
                    AppointmentServiceModel.service
                )
            )
            .order_by(AppointmentModel.created_at.desc())
        )

        if client_id is not None:
            stmt = stmt.where(AppointmentModel.client_id == client_id)
        if admin_id is not None:
            stmt = stmt.where(AppointmentModel.admin_id == admin_id)
        if status is not None:
            stmt = stmt.where(AppointmentModel.status == status)

        if date_filter is not None and date_filter in FUTURE_DATE_FILTERS:
            date_filter_timedelta = FUTURE_DATE_FILTERS[date_filter]
            now = datetime.now(UTC)
            stmt = stmt.where(
                AppointmentModel.date.between(now, now + date_filter_timedelta)
            )

        return await paginate(self.session, stmt, params)
