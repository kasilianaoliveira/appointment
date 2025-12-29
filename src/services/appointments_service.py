from uuid import UUID
from core.exceptions import AppointmentNotFoundException
from core.exceptions.appointment_exception import AppointmentsNotFoundException
from enums import AppointmentStatus, FutureDateFilter
from fastapi_pagination import Page, Params
from repositories.interfaces.appointments_interface import IAppointmentRepository
from models.appointment_model import AppointmentModel

from schemas.appointments_schema import AppointmentCreate


class AppointmentsService:
    def __init__(self, appointment_repository: IAppointmentRepository):
        self.appointment_repository = appointment_repository

    async def create_appointment(
        self,
        appointment: AppointmentCreate,
        client_id: UUID,
        admin_id: UUID | None = None,
    ) -> AppointmentModel:
        appointment_model = AppointmentModel(
            date=appointment.date,
            services=appointment.services,
            client_id=client_id,
            admin_id=admin_id,
        )
        return await self.appointment_repository.save(appointment_model)

    async def get_all_appointments(
        self,
        params: Params,
        client_id: UUID | None = None,
        admin_id: UUID | None = None,
        status: AppointmentStatus | None = None,
        date_filter: FutureDateFilter | None = None,
    ) -> Page[AppointmentModel]:
        appointments = await self.appointment_repository.get_all(
            params, client_id, admin_id, status, date_filter
        )

        if not appointments.items:
            return Page(items=[], total=0, page=params.page, size=params.size)

        return appointments
