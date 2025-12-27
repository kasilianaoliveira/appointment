from uuid import UUID
from core.exceptions.appointment_exception import AppointmentsNotFoundException
from fastapi_pagination import Page, Params
from repositories.interfaces.appointments_interface import IAppointmentRepository
from models.appointment_model import AppointmentModel

from schemas.appointments_schema import AppointmentCreate


class AppointmentsService:
    def __init__(self, appointment_repository: IAppointmentRepository):
        self.appointment_repository = appointment_repository

    async def create_appointment(
        self, appointment: AppointmentCreate
    ) -> AppointmentModel:
        appointment_model = AppointmentModel(
            date=appointment.date,
            services=appointment.services,
            client_id=appointment.client_id,
            admin_id=appointment.admin_id,
        )
        return await self.appointment_repository.save(appointment_model)

    async def get_all_appointments(self, params: Params) -> Page[AppointmentModel]:
        appointments = await self.appointment_repository.get_all(params)

        if not appointments:
            raise AppointmentsNotFoundException(detail="No appointments found")

        return appointments

    async def get_all_appointments_by_client_id(
        self, params: Params, client_id: UUID
    ) -> Page[AppointmentModel]:
        appointments = await self.appointment_repository.get_all_by_client_id(
            params, client_id
        )

        if not appointments:
            raise AppointmentsNotFoundException(detail="No appointments found")

        return appointments

    async def get_all_appointments_by_admin_id(
        self, params: Params, admin_id: UUID
    ) -> Page[AppointmentModel]:
        appointments = await self.appointment_repository.get_all_by_admin_id(
            params, admin_id
        )

        if not appointments:
            raise AppointmentsNotFoundException(detail="No appointments found")

        return appointments
