from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from core.security import oauth2_scheme
from models.user_model import UserModel
from schemas.token_schema import TokenSchema
from schemas.user_schema import UserCreate, UserRead
from services.auth_service import AuthService, get_auth_service
from services.user_service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserModel:
    """
    Extrai o token do header Authorization e retorna o usuário autenticado.
    """
    return await service.get_current_user(token)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.create_user(user)


@router.post(
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


@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_me(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """Retorna os dados do usuário autenticado."""
    return current_user
