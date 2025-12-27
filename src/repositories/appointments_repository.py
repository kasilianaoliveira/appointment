from datetime import UTC, datetime
from uuid import UUID
from enums import AppointmentStatus, DateFilter
from enums.date_filter import FutureDateFilter
from fastapi_pagination import Page, Params, paginate
from schemas import AppointmentCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import AppointmentModel
from repositories.interfaces.appointments_interface import IAppointmentsRepository
from sqlalchemy.orm import selectinload
from utils import DATE_FILTERS, FUTURE_DATE_FILTERS, get_date_filter


class AppointmentsRepository(IAppointmentsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, appointment: AppointmentModel) -> AppointmentModel:
        self.session.add(appointment)
        await self.session.commit()
        await self.session.refresh(appointment)
        return appointment

    async def update(self, appointment: AppointmentModel) -> AppointmentModel:
        self.session.add(appointment)
        await self.session.commit()
        await self.session.refresh(appointment)
        return appointment

    async def delete(self, appointment: AppointmentModel) -> None:
        await self.session.delete(appointment)
        await self.session.commit()

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
            .options(selectinload(AppointmentModel.services).selectinload("service"))
            .order_by(AppointmentModel.created_at)
        )

        if client_id:
            stmt = stmt.where(AppointmentModel.client_id == client_id)
        if admin_id:
            stmt = stmt.where(AppointmentModel.admin_id == admin_id)
        if status:
            stmt = stmt.where(AppointmentModel.status == status)

        if date_filter and date_filter in FUTURE_DATE_FILTERS:
            date_filter_timedelta = FUTURE_DATE_FILTERS[date_filter]
            stmt = stmt.where(
                AppointmentModel.date >= datetime.now(UTC) - date_filter_timedelta
            )

        return await paginate(self.session, stmt, params)

    async def get_all_by_client_id(
        self,
        params: Params,
        client_id: UUID,
        status: AppointmentStatus | None = None,
    ) -> Page[AppointmentModel]:
        stmt = (
            select(AppointmentModel)
            .options(selectinload(AppointmentModel.services).selectinload("service"))
            .where(AppointmentModel.client_id == client_id)
            .order_by(AppointmentModel.created_at)
        )
        if status:
            stmt = stmt.where(AppointmentModel.status == status)

        return await paginate(self.session, stmt, params)

    async def get_all_by_admin_id(
        self,
        params: Params,
        admin_id: UUID,
        status: AppointmentStatus | None = None,
    ) -> Page[AppointmentModel]:
        stmt = (
            select(AppointmentModel)
            .options(selectinload(AppointmentModel.services).selectinload("service"))
            .where(AppointmentModel.admin_id == admin_id)
            .order_by(AppointmentModel.created_at)
        )

        if status:
            stmt = stmt.where(AppointmentModel.status == status)

        return await paginate(self.session, stmt, params)
