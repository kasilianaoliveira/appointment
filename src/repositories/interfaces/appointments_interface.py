from abc import ABC, abstractmethod

from uuid import UUID

from enums import AppointmentStatus, FutureDateFilter
from fastapi_pagination import Page, Params
from models import AppointmentModel


class IAppointmentRepository(ABC):
    @abstractmethod
    async def save(self, appointment: AppointmentModel) -> AppointmentModel:
        pass

    @abstractmethod
    async def update(self, appointment: AppointmentModel) -> AppointmentModel:
        pass

    @abstractmethod
    async def delete(self, appointment: AppointmentModel) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> AppointmentModel | None:
        pass

    @abstractmethod
    async def get_all(
        self,
        params: Params,
        client_id: UUID | None = None,
        admin_id: UUID | None = None,
        status: AppointmentStatus | None = None,
        date_filter: FutureDateFilter | None = None,
    ) -> Page[AppointmentModel]:
        pass
