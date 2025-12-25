from abc import ABC, abstractmethod
from uuid import UUID

from models import ServiceModel
from schemas.services_schema import ServiceCreate, ServiceUpdate


class IServiceRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[ServiceModel]:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> ServiceModel | None:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> ServiceModel | None:
        pass

    @abstractmethod
    async def save(self, service: ServiceCreate) -> ServiceModel:
        pass

    @abstractmethod
    async def update(self, id: UUID, service: ServiceUpdate) -> ServiceModel:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        pass
