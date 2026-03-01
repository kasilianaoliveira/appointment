from abc import ABC, abstractmethod
from uuid import UUID

from fastapi_pagination import Page, Params

from enums import DateFilter
from models import UserModel


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: UserModel) -> UserModel:
        pass

    @abstractmethod
    async def update(self, user: UserModel) -> UserModel:
        pass

    @abstractmethod
    async def delete(self, user: UserModel) -> None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserModel | None:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> UserModel | None:
        pass

    @abstractmethod
    async def get_all_clients(
        self,
        params: Params,
        name: str | None = None,
        email: str | None = None,
        date_filter: DateFilter | None = None,
    ) -> Page[UserModel]:
        pass
