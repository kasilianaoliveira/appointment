from abc import ABC, abstractmethod
from uuid import UUID

from fastapi_pagination import Page, Params

from models.user_model import UserModel
from schemas.user_schema import UserCreate


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, data: UserCreate) -> UserModel:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserModel | None:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> UserModel | None:
        pass

    @abstractmethod
    async def get_all_clients(self, params: Params) -> Page[UserModel]:
        pass
