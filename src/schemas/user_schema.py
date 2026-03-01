from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from enums import UserRole
from enums.auth_provider import AuthProvider


class UserCreate(BaseModel):
    name: str
    password: str | None = None
    email: str
    phone: str
    role: UserRole
    auth_provider: AuthProvider = AuthProvider.LOCAL


class UserRead(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
