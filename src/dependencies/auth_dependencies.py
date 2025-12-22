from typing import Annotated

from fastapi import Depends, HTTPException

from core.security import oauth2_scheme
from enums import UserRole
from models import UserModel
from services.auth_service import AuthService, get_auth_service


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserModel:
    """
    Extrai o token do header Authorization e retorna o usuário autenticado.
    """
    return await service.get_current_user(token)


def require_admin_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="User not authorized")
    return current_user
