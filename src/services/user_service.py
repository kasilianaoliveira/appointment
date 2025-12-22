import logging
from uuid import UUID

from fastapi import Depends
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.dependencies import get_session
from core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    UsersNotFoundException,
)
from core.security import (
    get_password_hash,
)
from enums import UserDateFilter
from models import UserModel
from repositories.interfaces.user_interface import IUserRepository
from repositories.user_repository import UserRepository
from schemas import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate) -> UserModel:

        existing_user = await self.user_repository.get_by_email(user.email)

        if existing_user:
            raise UserAlreadyExistsException(
                detail=f"User with email {user.email} already exists"
            )

        logger.info(f"Creating user: {user}")
        user.password_hash = get_password_hash(user.password_hash)

        return await self.user_repository.save(user)

    async def update_user(self, id: UUID, user: UserUpdate) -> UserModel:
        existing_user = await self.user_repository.get_by_id(id)

        if not existing_user:
            raise UserNotFoundException(detail=f"User with id {id} not found")

        if user.name is not None:
            existing_user.name = user.name

        if user.email is not None:
            existing_user.email = user.email

        if user.phone is not None:
            existing_user.phone = user.phone

        return await self.user_repository.update(existing_user)

    async def delete_user(self, id: UUID) -> None:
        existing_user = await self.user_repository.get_by_id(id)

        if not existing_user:
            raise UserNotFoundException(detail=f"User with id {id} not found")

        return await self.user_repository.delete(existing_user)

    async def get_user_by_email(self, email: str) -> UserModel | None:

        existing_user = await self.user_repository.get_by_email(email)

        if not existing_user:
            raise UserNotFoundException(
                detail=f"User with email {email} not found",
            )

        logger.info(f"User email found: {existing_user}")
        return existing_user

    async def get_user_by_id(self, id: UUID) -> UserModel | None:
        existing_user = await self.user_repository.get_by_id(id)

        if not existing_user:
            raise UserNotFoundException(detail=f"User with id {id} not found")

        logger.info(f"User id found: {existing_user}")

        return existing_user

    async def get_all_clients(
        self,
        params: Params,
        name: str | None = None,
        email: str | None = None,
        date_filter: UserDateFilter | None = None,
    ) -> Page[UserModel]:

        existing_users = await self.user_repository.get_all_clients(
            params, name, email, date_filter
        )

        if not existing_users:
            raise UsersNotFoundException(
                detail="No users found matching the provided criteria"
            )

        logger.info(f"Users found: {existing_users}")

        return existing_users


def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)
