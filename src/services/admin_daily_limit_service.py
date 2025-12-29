import logging
from uuid import UUID
from core.db.dependencies import get_session
from core.exceptions import (
    AdminDailyLimitAlreadyExistsException,
    AdminDailyLimitNotFoundException,
)
from fastapi import Depends
from models.admin_daily_limit_model import AdminDailyLimitModel
from repositories.admin_daily_limit_repository import AdminDailyLimitRepository
from repositories.interfaces.admin_daily_limit_interface import (
    IAdminDailyLimitRepository,
)
from schemas.admin_daily_limit_schema import (
    AdminDailyLimitCreate,
    AdminDailyLimitUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AdminDailyLimitService:
    def __init__(self, admin_daily_limit_repository: IAdminDailyLimitRepository):
        self.admin_daily_limit_repository = admin_daily_limit_repository

    async def get_admin_daily_limit_by_id(self, id: UUID) -> AdminDailyLimitModel:
        existing_admin_daily_limit = await self.admin_daily_limit_repository.get_by_id(
            id
        )
        if not existing_admin_daily_limit:
            raise AdminDailyLimitNotFoundException(
                detail=f"Admin daily limit with id {id} not found",
            )
        logger.info(f"Admin daily limit found: {existing_admin_daily_limit}")
        return existing_admin_daily_limit

    async def get_all_admin_daily_limits(self) -> list[AdminDailyLimitModel]:
        existing_admin_daily_limits = await self.admin_daily_limit_repository.get_all()
        if not existing_admin_daily_limits:
            raise AdminDailyLimitNotFoundException(
                detail="No admin daily limits found",
            )
        logger.info(f"Admin daily limits found: {existing_admin_daily_limits}")
        return existing_admin_daily_limits

    async def create_admin_daily_limit(
        self, admin_daily_limit: AdminDailyLimitCreate, admin_id: UUID
    ) -> AdminDailyLimitModel:
        existing_admin_daily_limit = (
            await self.admin_daily_limit_repository.get_by_week_day(
                admin_daily_limit.week_day
            )
        )
        if existing_admin_daily_limit:
            raise AdminDailyLimitAlreadyExistsException(
                detail=f"Admin daily limit with week day {admin_daily_limit.week_day} already exists",
            )
        admin_daily_limit_model = AdminDailyLimitModel(
            admin_id=admin_id,
            week_day=admin_daily_limit.week_day,
            limit=admin_daily_limit.limit,
        )
        logger.info(f"Admin daily limit created: {admin_daily_limit_model}")
        return await self.admin_daily_limit_repository.save(admin_daily_limit_model)

    async def update_admin_daily_limit(
        self, id: UUID, admin_daily_limit: AdminDailyLimitUpdate
    ) -> AdminDailyLimitModel:
        existing_admin_daily_limit = await self.admin_daily_limit_repository.get_by_id(
            id
        )
        if not existing_admin_daily_limit:
            raise AdminDailyLimitNotFoundException(
                detail=f"Admin daily limit with id {id} not found",
            )
        existing_admin_daily_limit.week_day = admin_daily_limit.week_day
        existing_admin_daily_limit.limit = admin_daily_limit.limit
        logger.info(f"Admin daily limit updated: {existing_admin_daily_limit}")
        return await self.admin_daily_limit_repository.update(
            existing_admin_daily_limit
        )

    async def delete_admin_daily_limit(self, id: UUID) -> None:
        existing_admin_daily_limit = await self.admin_daily_limit_repository.get_by_id(
            id
        )
        if not existing_admin_daily_limit:
            raise AdminDailyLimitNotFoundException(
                detail=f"Admin daily limit with id {id} not found",
            )
        logger.info(f"Admin daily limit deleted: {existing_admin_daily_limit}")
        return await self.admin_daily_limit_repository.delete(
            existing_admin_daily_limit
        )


def get_admin_daily_limit_service(
    db: AsyncSession = Depends(get_session),
) -> AdminDailyLimitService:
    repo = AdminDailyLimitRepository(db)
    return AdminDailyLimitService(repo)
