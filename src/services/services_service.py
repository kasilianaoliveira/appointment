import logging
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.dependencies import get_session
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service with this name already exists",
            )
        logger.info(f"Creating service: {service}")
        return await self.services_repository.save(service)

    async def update_service(
        self,
        id: UUID,
        service: ServiceUpdate,
    ) -> ServiceModel:
        existing_service = await self.services_repository.get_by_id(id)

        if not existing_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )

        logger.info(f"Updating service: {service}")
        return await self.services_repository.update(id, service)

    async def delete_service(self, id: UUID) -> None:
        existing_service = await self.services_repository.get_by_id(id)

        if not existing_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )
        logger.info(f"Deleting service: {id}")
        return await self.services_repository.delete(existing_service)

    async def get_service_by_id(self, id: UUID) -> ServiceModel:
        existing_service = await self.services_repository.get_by_id(id)

        if not existing_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )
        logger.info(f"Getting service by id: {id}")
        return existing_service

    async def get_all_services(self) -> list[ServiceModel]:
        existing_services = await self.services_repository.get_all()

        if not existing_services:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No services found",
            )
        logger.info("Getting all services")
        return existing_services


def get_services_service(
    db: AsyncSession = Depends(get_session),
) -> ServicesService:
    repo = ServicesRepository(db)
    return ServicesService(repo)
