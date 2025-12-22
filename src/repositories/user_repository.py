from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enums.user_date_filter import UserDateFilter
from enums.user_role import UserRole
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

    async def update(self, user: UserModel) -> UserModel:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: UserModel) -> None:

        await self.session.delete(user)
        await self.session.commit()

    async def get_all_clients(
        self,
        params: Params,
        name: str | None = None,
        email: str | None = None,
        date_filter: UserDateFilter | None = None,
    ) -> Page[UserModel]:
        stmt = (
            select(UserModel)
            .order_by(UserModel.created_at)
            .where(UserModel.role == UserRole.CLIENT)
        )

        # like = case sensitive
        # ilike = case insensitive

        if name:
            stmt = stmt.where(UserModel.name.ilike(f"%{name}%"))
        if email:
            stmt = stmt.where(UserModel.email.ilike(f"%{email}%"))

        DATA_FILTERS = {
            UserDateFilter.LAST_7_DAYS: timedelta(days=7),
            UserDateFilter.LAST_30_DAYS: timedelta(days=30),
            UserDateFilter.LAST_90_DAYS: timedelta(days=90),
        }

        if date_filter and date_filter in DATA_FILTERS:
            stmt = stmt.where(
                UserModel.created_at >= datetime.now(UTC) - DATA_FILTERS[date_filter]
            )
        return await paginate(self.session, stmt, params)
