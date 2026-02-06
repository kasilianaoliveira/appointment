from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, Params

from dependencies.auth_dependencies import get_current_user, require_admin_user
from dependencies.pagination_dependencies import get_pagination_params
from enums import DateFilter
from models import UserModel
from schemas import TokenSchema, UserCreate, UserRead, UserUpdate
from services.auth_service import AuthService, get_auth_service
from services.user_service import UserService, get_user_service

user_public_router = APIRouter(prefix="/users", tags=["Users"])


protected_user_router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


@user_public_router.post(
    "/", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.create_user(user)


@protected_user_router.put(
    "/{id}", response_model=UserRead, status_code=status.HTTP_200_OK
)
async def update_user(
    id: UUID,
    user: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.update_user(id, user)


@protected_user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.delete_user(id)


@protected_user_router.get(
    "/detail/{id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
    _: Annotated[UserModel, Depends(require_admin_user)],
):
    return await service.get_user_by_id(id)


@protected_user_router.get(
    "/", response_model=Page[UserRead], status_code=status.HTTP_200_OK
)
async def get_all_clients(
    params: Annotated[Params, Depends(get_pagination_params)],
    service: Annotated[UserService, Depends(get_user_service)],
    _: Annotated[UserModel, Depends(require_admin_user)],
    name: str | None = None,
    email: str | None = None,
    date_filter: DateFilter | None = None,
):
    return await service.get_all_clients(params, name, email, date_filter)
