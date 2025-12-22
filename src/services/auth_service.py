import logging

import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.dependencies import get_session
from core.security import create_access_token, verify_password
from core.settings import get_settings
from models import UserModel
from repositories.interfaces.user_interface import IUserRepository
from repositories.user_repository import UserRepository
from schemas import TokenSchema

settings = get_settings()

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> TokenSchema:
        existing_user = await self.user_repository.get_by_email(email)

        if not existing_user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
            )

        if not verify_password(password, existing_user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
            )
        logger.info(f"User authenticated: {existing_user}")

        token, expires_in = create_access_token(
            {"sub": str(existing_user.id)},
        )
        return TokenSchema(
            access_token=token,
            token_type="bearer",
            expires_in=expires_in,
        )

    async def get_current_user(
        self,
        token: str,
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY.get_secret_value(),
                algorithms=[settings.JWT_ALGORITHM],
            )
            user_id = payload.get("sub")

            if user_id is None:
                raise credentials_exception

        except jwt.InvalidTokenError:
            raise credentials_exception

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    def get_current_active_user(current_user: UserModel) -> UserModel:
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user


def get_auth_service(db: AsyncSession = Depends(get_session)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)
