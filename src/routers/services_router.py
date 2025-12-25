from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from dependencies.auth_dependencies import require_admin_user
from schemas.services_schema import ServiceCreate, ServiceRead, ServiceUpdate
from services.services_service import ServicesService, get_services_service

services_router = APIRouter(
    prefix="/services",
    tags=["Services"],
    dependencies=[
        Depends(require_admin_user),
    ],
)


@services_router.post(
    "/",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    data: ServiceCreate,
    service: Annotated[ServicesService, Depends(get_services_service)],
):
    return await service.create_service(data)


@services_router.put(
    "/{id}",
    response_model=ServiceRead,
    status_code=status.HTTP_200_OK,
)
async def update_service(
    id: UUID,
    data: ServiceUpdate,
    service: Annotated[ServicesService, Depends(get_services_service)],
):
    return await service.update_service(id, data)


@services_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(
    id: UUID,
    service: Annotated[ServicesService, Depends(get_services_service)],
):
    return await service.delete_service(id)


@services_router.get(
    "/{id}",
    response_model=ServiceRead,
    status_code=status.HTTP_200_OK,
)
async def get_service_by_id(
    id: UUID,
    service: Annotated[ServicesService, Depends(get_services_service)],
):
    return await service.get_service_by_id(id)


@services_router.get(
    "/",
    response_model=list[ServiceRead],
    status_code=status.HTTP_200_OK,
)
async def get_all_services(
    service: Annotated[ServicesService, Depends(get_services_service)],
):
    return await service.get_all_services()
