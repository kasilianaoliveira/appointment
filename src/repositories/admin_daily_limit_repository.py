from uuid import UUID
from enums import WeekDay
from models import AdminDailyLimitModel
from repositories.interfaces.admin_daily_limit_interface import (
    IAdminDailyLimitRepository,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AdminDailyLimitRepository(IAdminDailyLimitRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> AdminDailyLimitModel | None:
        result = await self.session.execute(
            select(AdminDailyLimitModel).where(AdminDailyLimitModel.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_week_day(
        self, admin_id: UUID, week_day: WeekDay
    ) -> AdminDailyLimitModel | None:
        result = await self.session.execute(
            select(AdminDailyLimitModel).where(
                AdminDailyLimitModel.admin_id == admin_id,
                AdminDailyLimitModel.week_day == week_day,
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[AdminDailyLimitModel]:
        result = await self.session.execute(select(AdminDailyLimitModel))
        return result.scalars().all()

    async def save(
        self, admin_daily_limit: AdminDailyLimitModel
    ) -> AdminDailyLimitModel:
        self.session.add(admin_daily_limit)
        await self.session.commit()
        await self.session.refresh(admin_daily_limit)
        return admin_daily_limit

    async def update(
        self, admin_daily_limit: AdminDailyLimitModel
    ) -> AdminDailyLimitModel:
        self.session.add(admin_daily_limit)
        await self.session.commit()
        await self.session.refresh(admin_daily_limit)
        return admin_daily_limit

    async def delete(self, admin_daily_limit: AdminDailyLimitModel) -> None:
        await self.session.delete(admin_daily_limit)
        await self.session.commit()
