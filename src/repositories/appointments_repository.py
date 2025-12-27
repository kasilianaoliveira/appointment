from uuid import UUID
from schemas import AppointmentCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import AppointmentModel
from repositories.interfaces.appointments_interface import IAppointmentsRepository


class AppointmentsRepository(IAppointmentsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, appointment: AppointmentCreate) -> AppointmentModel:
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

    async def get_by_client_id(self, client_id: UUID) -> AppointmentModel | None:
        result = await self.session.execute(
            select(AppointmentModel).where(AppointmentModel.client_id == client_id)
        )
        return result.scalar_one_or_none()

    async def get_by_admin_id(self, admin_id: UUID) -> AppointmentModel | None:
        result = await self.session.execute(
            select(AppointmentModel).where(AppointmentModel.admin_id == admin_id)
        )
        return result.scalar_one_or_none()
