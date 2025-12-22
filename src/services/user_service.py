import logging
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.dependencies import get_session
from core.security import (
    get_password_hash,
)
from models.user_model import UserModel
from repositories.interfaces.user_interface import IUserRepository
from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreate

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate) -> UserModel:

        existing_user = await self.user_repository.get_by_email(user.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        logger.info(f"Creating user: {user}")
        user.password_hash = get_password_hash(user.password_hash)

        return await self.user_repository.save(user)

    async def get_user_by_email(self, email: str) -> UserModel | None:

        existing_user = await self.user_repository.get_by_email(email)

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"User email found: {existing_user}")
        return existing_user

    async def get_user_by_id(self, id: UUID) -> UserModel | None:
        existing_user = await self.user_repository.get_by_id(id)

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"User id found: {existing_user}")

        return existing_user

    async def get_all_clients(
        self,
        params: Params,
    ) -> Page[UserModel]:

        existing_users = await self.user_repository.get_all_clients(params)

        if not existing_users:
            raise HTTPException(status_code=404, detail="Users not found")

        logger.info(f"Users found: {existing_users}")

        return existing_users


def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)
