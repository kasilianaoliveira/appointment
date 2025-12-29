from abc import ABC, abstractmethod
from uuid import UUID
from enums import WeekDay
from models.admin_daily_limit_model import AdminDailyLimitModel


class IAdminDailyLimitRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: UUID) -> AdminDailyLimitModel | None:
        pass

    @abstractmethod
    async def get_by_week_day(
        self, admin_id: UUID, week_day: WeekDay
    ) -> AdminDailyLimitModel | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[AdminDailyLimitModel]:
        pass

    @abstractmethod
    async def save(
        self, admin_daily_limit: AdminDailyLimitModel
    ) -> AdminDailyLimitModel:
        pass

    @abstractmethod
    async def update(
        self, admin_daily_limit: AdminDailyLimitModel
    ) -> AdminDailyLimitModel:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        pass
