from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from src.dependencies.auth_dependencies import get_current_user
from src.models import UserModel
from src.schemas import TokenSchema, UserRead
from src.services.auth_service import AuthService, get_auth_service
from fastapi.security import OAuth2PasswordRequestForm

auth_public_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_public_router.post(
    "/login",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Autentica o usuário e retorna um token JWT."""
    token_data = await service.authenticate_user(
        form_data.username,
        form_data.password,
    )
    return token_data


@auth_public_router.get(
    "/me", response_model=UserRead, status_code=status.HTTP_200_OK
)
async def get_me(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """Retorna os dados do usuário autenticado."""
    return current_user
