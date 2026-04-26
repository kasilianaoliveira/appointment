from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials

from core.security import AUTH_COOKIE_NAME, oauth2_scheme
from enums import UserRole
from models import UserModel
from services.auth_service import AuthService, get_auth_service


async def get_current_user(
    request: Request,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(oauth2_scheme)
    ],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserModel:
    """
    Extrai o token do header Authorization ou de cookie e retorna o usuário autenticado.
    """
    token = credentials.credentials if credentials else None

    if token is None:
        token = request.cookies.get(AUTH_COOKIE_NAME)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await service.get_current_user(token)


def require_admin_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="User not authorized")
    return current_user
