import logging
from decimal import Decimal
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.dependencies import get_session
from core.exceptions import (
    ServiceAlreadyExistsException,
    ServiceNotFoundException,
    ServicesNotFoundException,
)
from core.exceptions.services_exception import InvalidServicePriceException
from models import ServiceModel
from repositories.interfaces.services_interface import IServiceRepository
from repositories.services_repository import ServicesRepository
from schemas.services_schema import ServiceCreate, ServiceUpdate

logger = logging.getLogger(__name__)


class ServicesService:
    def __init__(self, services_repository: IServiceRepository):
        self.services_repository = services_repository

    async def create_service(self, service: ServiceCreate) -> ServiceModel:
        existing_service = await self.services_repository.get_by_name(
            service.name,
        )

        if existing_service:
            raise ServiceAlreadyExistsException(
                detail=f"Service with name '{service.name}' already exists"
            )

        if service.price <= 0:
            raise InvalidServicePriceException(
                detail="Service price must be greater than 0"
            )

        service_model = ServiceModel(
            name=service.name,
            description=service.description,
            price=Decimal(str(service.price)),
        )

        logger.info(f"Creating service name={service.name}")
        return await self.services_repository.save(service_model)

    async def update_service(
        self,
        id: UUID,
        service: ServiceUpdate,
    ) -> ServiceModel:
        existing_service = await self.services_repository.get_by_id(id)

        if not existing_service:
            raise ServiceNotFoundException(
                detail=f"Service with id {id} not found",
            )

        if service.name is not None:
            existing_service.name = service.name

        if service.description is not None:
            existing_service.description = service.description

        if service.price is not None:
            existing_service.price = service.price

        logger.info(f"Updating service: {service}")
        return await self.services_repository.update(id, service)

    async def delete_service(self, id: UUID) -> None:
        existing_service = await self.services_repository.get_by_id(id)

        if not existing_service:
            raise ServiceNotFoundException(
                detail=f"Service with id {id} not found",
            )
        logger.info(f"Deleting service: {id}")
        return await self.services_repository.delete(existing_service)

    async def get_service_by_id(self, id: UUID) -> ServiceModel:
        existing_service = await self.services_repository.get_by_id(id)

        if not existing_service:
            raise ServiceNotFoundException(
                detail=f"Service with id {id} not found",
            )
        logger.info(f"Getting service by id: {id}")
        return existing_service

    async def get_all_services(self) -> list[ServiceModel]:
        existing_services = await self.services_repository.get_all()

        if not existing_services:
            raise ServicesNotFoundException(detail="No services found")
        logger.info("Getting all services")
        return existing_services


def get_services_service(
    db: AsyncSession = Depends(get_session),
) -> ServicesService:
    repo = ServicesRepository(db)
    return ServicesService(repo)
