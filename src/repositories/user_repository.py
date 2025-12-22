from uuid import UUID

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import UserModel
from repositories.interfaces.user_interface import IUserRepository
from schemas.user_schema import UserCreate


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, data: UserCreate) -> UserModel:

        user = UserModel(
            name=data.name,
            password_hash=data.password_hash,
            email=data.email,
            phone=data.phone,
            role=data.role,
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, id: UUID) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == id),
        )
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, limit: int = 10) -> Page[UserModel]:
        stmt = select(UserModel).order_by(UserModel.created_at)
        return await paginate(self.session, stmt, page=page, limit=limit)
