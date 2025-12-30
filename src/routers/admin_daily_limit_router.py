from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from models import UserModel
from routers.user_router import require_admin_user
from schemas.admin_daily_limit_schema import (
    AdminDailyLimitCreate,
    AdminDailyLimitRead,
    AdminDailyLimitUpdate,
)
from services.admin_daily_limit_service import (
    AdminDailyLimitService,
    get_admin_daily_limit_service,
)

protected_admin_daily_router = APIRouter(
    prefix="/admin_daily_limits",
    tags=["Admin Daily Limits"],
    dependencies=[Depends(require_admin_user)],
)


@protected_admin_daily_router.get(
    "/",
    response_model=List[AdminDailyLimitRead],
    status_code=status.HTTP_200_OK,
)
async def get_all_admin_daily_limits(
    service: Annotated[
        AdminDailyLimitService,
        Depends(
            get_admin_daily_limit_service,
        ),
    ],
):
    return await service.get_all_admin_daily_limits()


@protected_admin_daily_router.get(
    "/{id}",
    response_model=AdminDailyLimitRead,
    status_code=status.HTTP_200_OK,
)
async def get_admin_daily_limit_by_id(
    id: UUID,
    service: Annotated[
        AdminDailyLimitService,
        Depends(
            get_admin_daily_limit_service,
        ),
    ],
):
    return await service.get_admin_daily_limit_by_id(id)


@protected_admin_daily_router.post(
    "/",
    response_model=AdminDailyLimitRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_admin_daily_limit(
    admin_daily_limit: AdminDailyLimitCreate,
    current_user: Annotated[UserModel, Depends(require_admin_user)],
    service: Annotated[
        AdminDailyLimitService,
        Depends(
            get_admin_daily_limit_service,
        ),
    ],
):
    return await service.create_admin_daily_limit(
        admin_daily_limit,
        current_user.id,
    )


@protected_admin_daily_router.put(
    "/{id}",
    response_model=AdminDailyLimitRead,
    status_code=status.HTTP_200_OK,
)
async def update_admin_daily_limit(
    id: UUID,
    admin_daily_limit: AdminDailyLimitUpdate,
    service: Annotated[
        AdminDailyLimitService,
        Depends(
            get_admin_daily_limit_service,
        ),
    ],
):
    return await service.update_admin_daily_limit(id, admin_daily_limit)


@protected_admin_daily_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_admin_daily_limit(
    id: UUID,
    service: Annotated[
        AdminDailyLimitService,
        Depends(
            get_admin_daily_limit_service,
        ),
    ],
):
    return await service.delete_admin_daily_limit(id)
