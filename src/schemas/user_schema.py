from uuid import UUID

from pydantic import BaseModel

from enums import UserRole


class UserCreate(BaseModel):
    name: str
    password: str
    email: str
    phone: str
    role: UserRole


class UserRead(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str
    role: UserRole

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
