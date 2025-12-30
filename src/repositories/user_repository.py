from datetime import UTC, datetime
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enums import DateFilter, UserRole
from models import UserModel
from repositories.interfaces.user_interface import IUserRepository
from utils import DATE_FILTERS
from utils.date_filters import get_date_filter


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: UserModel) -> UserModel:

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
        merged_user = await self.session.merge(user)
        await self.session.commit()
        await self.session.refresh(merged_user)
        return merged_user

    async def delete(self, user: UserModel) -> None:

        await self.session.delete(user)
        await self.session.commit()

    async def get_all_clients(
        self,
        params: Params,
        name: str | None = None,
        email: str | None = None,
        date_filter: DateFilter | None = None,
    ) -> Page[UserModel]:
        stmt = (
            select(UserModel)
            .order_by(UserModel.created_at)
            .where(UserModel.role == UserRole.CLIENT)
        )

        if name:
            stmt = stmt.where(UserModel.name.ilike(f"%{name}%"))
        if email:
            stmt = stmt.where(UserModel.email.ilike(f"%{email}%"))

        if date_filter and date_filter in DATE_FILTERS:
            date_filter_timedelta = get_date_filter(date_filter)
            stmt = stmt.where(
                UserModel.created_at >= datetime.now(UTC) - date_filter_timedelta
            )
        return await paginate(self.session, stmt, params)
