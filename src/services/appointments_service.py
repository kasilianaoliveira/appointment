from datetime import UTC, datetime
from uuid import UUID

from fastapi import Depends
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.dependencies import get_session
from core.exceptions import (
    AppointmentNotFoundException,
    InvalidAppointmentStateException,
)
from enums import AppointmentStatus, FutureDateFilter
from models.appointment_model import AppointmentModel
from models.appointment_service_model import AppointmentServiceModel
from repositories.appointments_repository import AppointmentsRepository
from repositories.interfaces.appointments_interface import (
    IAppointmentRepository,
)
from schemas.appointments_schema import (
    AppointmentClientUpdate,
    AppointmentCreate,
)


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
            client_id=client_id,
            admin_id=admin_id,
        )

        for service_id in appointment.services:
            appointment_service = AppointmentServiceModel(
                appointment_id=appointment_model.id,
                service_id=service_id,
            )
            appointment_model.services.append(appointment_service)

        return await self.appointment_repository.save(appointment_model)

    async def delete_appointment(self, id: UUID) -> None:
        existing_appointment = await self.appointment_repository.get_by_id(id)
        if not existing_appointment:
            raise AppointmentNotFoundException(
                detail=f"Appointment with id {id} not found",
            )
        return await self.appointment_repository.delete(existing_appointment)

    async def update_by_client(
        self,
        appointment_id: UUID,
        appointment: AppointmentClientUpdate,
        client_id: UUID | None = None,
    ) -> AppointmentModel:
        existing_appointment = await self.appointment_repository.get_by_id(
            appointment_id
        )
        if not existing_appointment:
            raise AppointmentNotFoundException(
                detail=f"Appointment with id {appointment_id} not found",
            )

        if existing_appointment.client_id != client_id:
            raise InvalidAppointmentStateException(
                detail=f"Appointment with id {appointment_id} does not belong to the client",
            )

        if existing_appointment.status != AppointmentStatus.PENDING:
            raise InvalidAppointmentStateException(
                detail=f"Appointment with id {appointment_id} is not pending",
            )

        if appointment.date is not None:
            existing_appointment.date = appointment.date

        if appointment.services is not None:
            existing_appointment.services.clear()

            for service_id in appointment.services:
                appointment_service = AppointmentServiceModel(
                    appointment_id=existing_appointment.id,
                    service_id=service_id,
                )
                existing_appointment.services.append(appointment_service)

        return await self.appointment_repository.update(existing_appointment)

    async def cancel_appointment(
        self,
        appointment_id: UUID,
        cancel_reason: str,
        client_id: UUID | None = None,
        admin_id: UUID | None = None,
    ) -> AppointmentModel:
        existing_appointment = await self.appointment_repository.get_by_id(
            appointment_id
        )
        if not existing_appointment:
            raise AppointmentNotFoundException(
                detail=f"Appointment with id {appointment_id} not found",
            )

        is_client = (
            client_id is not None and existing_appointment.client_id == client_id
        )
        is_admin = admin_id is not None and existing_appointment.admin_id == admin_id

        if not (is_client or is_admin):
            raise InvalidAppointmentStateException(
                detail=f"Appointment with id {appointment_id} can only be cancelled by the client or assigned admin",
            )

        if existing_appointment.status not in {
            AppointmentStatus.PENDING,
            AppointmentStatus.CONFIRMED,
        }:
            raise InvalidAppointmentStateException(
                detail="This appointment cannot be cancelled",
            )

        existing_appointment.status = AppointmentStatus.CANCELLED
        existing_appointment.cancel_reason = cancel_reason
        existing_appointment.cancelled_at = datetime.now(UTC)

        return await self.appointment_repository.update(existing_appointment)

    async def confirm_by_admin(
        self,
        appointment_id: UUID,
        admin_id: UUID | None = None,
    ) -> AppointmentModel:
        if admin_id is None:
            raise InvalidAppointmentStateException(
                detail="Admin ID is required to confirm an appointment",
            )

        existing_appointment = await self.appointment_repository.get_by_id(
            appointment_id
        )
        if not existing_appointment:
            raise AppointmentNotFoundException(
                detail=f"Appointment with id {appointment_id} not found",
            )

        if existing_appointment.status == AppointmentStatus.CANCELLED:
            raise InvalidAppointmentStateException(
                detail=f"Appointment with id {appointment_id} is cancelled",
            )

        if existing_appointment.status == AppointmentStatus.CONFIRMED:
            raise InvalidAppointmentStateException(
                detail=f"Appointment with id {appointment_id} is already confirmed",
            )

        if existing_appointment.admin_id is not None:
            if existing_appointment.admin_id != admin_id:
                raise InvalidAppointmentStateException(
                    detail=f"Appointment with id {appointment_id} is already assigned to a different admin",
                )
        else:
            existing_appointment.admin_id = admin_id
            existing_appointment.status = AppointmentStatus.CONFIRMED

        return await self.appointment_repository.update(existing_appointment)

    async def get_appointment_by_id(
        self,
        appointment_id: UUID,
    ) -> AppointmentModel:
        appointment = await self.appointment_repository.get_by_id(appointment_id)
        if not appointment:
            raise AppointmentNotFoundException(
                detail=f"Appointment with id {appointment_id} not found",
            )
        return appointment

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


def get_appointments_service(
    db: AsyncSession = Depends(get_session),
) -> AppointmentsService:
    repo = AppointmentsRepository(db)
    return AppointmentsService(repo)
