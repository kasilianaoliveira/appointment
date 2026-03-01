from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from core.oauth import oauth
from core.settings import get_settings
from src.dependencies.auth_dependencies import get_current_user
from src.models import UserModel
from src.schemas import TokenSchema, UserRead
from src.services.auth_service import AuthService, get_auth_service

auth_public_router = APIRouter(prefix="/auth", tags=["Auth"])

settings = get_settings()


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


@auth_public_router.get("/google")
async def google_login(request: Request):

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )


@auth_public_router.get("/google/callback")
async def google_callback(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    token = await oauth.google.authorize_access_token(request)

    user_info = await oauth.google.parse_id_token(request, token)
    user_info2 = token.get("userinfo")
    print("User info:", user_info)
    print("User info from token:", user_info2)

    email = user_info2["email"]
    name = user_info2.get("name")

    return await auth_service.authenticate_google_user(email=email, name=name)
