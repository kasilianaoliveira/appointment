from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params

from dependencies.auth_dependencies import get_current_user, require_admin_user
from dependencies.pagination_dependencies import get_pagination_params
from enums import AppointmentStatus, FutureDateFilter, UserRole
from models import UserModel
from schemas.appointments_schema import (
    AppointmentAdminUpdate,
    AppointmentCancel,
    AppointmentClientUpdate,
    AppointmentCreate,
    AppointmentRead,
)
from services.appointments_service import (
    AppointmentsService,
    get_appointments_service,
)

protected_user_router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    dependencies=[Depends(get_current_user)],
)

protected_admin_router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    dependencies=[Depends(require_admin_user)],
)


@protected_user_router.post(
    "/",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    appointment: AppointmentCreate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[AppointmentsService, Depends(get_appointments_service)],
):
    return await service.create_appointment(appointment, current_user.id)


@protected_user_router.get(
    "/{id}",
    response_model=AppointmentRead,
    status_code=status.HTTP_200_OK,
)
async def get_appointment_by_id(
    id: UUID,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[AppointmentsService, Depends(get_appointments_service)],
):
    """Busca um appointment por ID."""
    appointment = await service.get_appointment_by_id(id)

    if (
        current_user.role != UserRole.ADMIN
        and appointment.client_id != current_user.id
        and appointment.admin_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail="You don't have permission to view this appointment"
        )
    return appointment


@protected_user_router.get(
    "/",
    response_model=Page[AppointmentRead],
    status_code=status.HTTP_200_OK,
)
async def get_all_appointments(
    params: Annotated[Params, Depends(get_pagination_params)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[AppointmentsService, Depends(get_appointments_service)],
    status: AppointmentStatus | None = None,
    date_filter: FutureDateFilter | None = None,
):
    client_id = None if current_user.role == UserRole.ADMIN else current_user.id
    admin_id = current_user.id if current_user.role == UserRole.ADMIN else None

    return await service.get_all_appointments(
        params=params,
        client_id=client_id,
        admin_id=admin_id,
        status=status,
        date_filter=date_filter,
    )


@protected_user_router.put(
    "/{id}",
    response_model=AppointmentRead,
    status_code=status.HTTP_200_OK,
)
async def update_appointment_by_client(
    id: UUID,
    appointment: AppointmentClientUpdate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[AppointmentsService, Depends(get_appointments_service)],
):
    """Atualiza um appointment (apenas cliente, apenas quando está PENDING)."""
    return await service.update_by_client(id, appointment, current_user.id)


@protected_user_router.post(
    "/{id}/cancel",
    response_model=AppointmentRead,
    status_code=status.HTTP_200_OK,
)
async def cancel_appointment(
    id: UUID,
    cancel_data: AppointmentCancel,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[AppointmentsService, Depends(get_appointments_service)],
):

    client_id = current_user.id if current_user.role == UserRole.CLIENT else None
    admin_id = current_user.id if current_user.role == UserRole.ADMIN else None

    return await service.cancel_appointment(
        appointment_id=id,
        cancel_reason=cancel_data.cancel_reason,
        client_id=client_id,
        admin_id=admin_id,
    )


@protected_admin_router.post(
    "/{id}/confirm",
    response_model=AppointmentRead,
    status_code=status.HTTP_200_OK,
)
async def confirm_appointment_by_admin(
    id: UUID,
    current_user: Annotated[UserModel, Depends(require_admin_user)],
    service: Annotated[AppointmentsService, Depends(get_appointments_service)],
):
    return await service.confirm_by_admin(id, current_user.id)


@protected_admin_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_appointment(
    id: UUID,
    service: Annotated[AppointmentsService, Depends(get_appointments_service)],
):
    return await service.delete_appointment(id)
