from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import ServiceModel
from repositories.interfaces.services_interface import IServiceRepository
from schemas.services_schema import ServiceCreate, ServiceUpdate


class ServicesRepository(IServiceRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[ServiceModel]:
        result = await self.session.execute(
            select(ServiceModel).order_by(ServiceModel.created_at)
        )
        return result.scalars().all()

    async def get_by_id(self, id: UUID) -> ServiceModel | None:
        result = await self.session.execute(
            select(ServiceModel).where(ServiceModel.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> ServiceModel | None:
        result = await self.session.execute(
            select(ServiceModel).where(ServiceModel.name == name)
        )
        return result.scalar_one_or_none()

    async def save(self, service: ServiceModel) -> ServiceModel:

        self.session.add(service)
        await self.session.commit()
        await self.session.refresh(service)
        return service

    async def update(self, id: UUID, data: ServiceUpdate) -> ServiceModel:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def delete(self, data: ServiceModel) -> None:
        await self.session.delete(data)
        await self.session.commit()
