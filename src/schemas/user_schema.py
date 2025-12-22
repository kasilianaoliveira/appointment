from uuid import UUID

from pydantic import BaseModel

from models.user_role import UserRole


class UserCreate(BaseModel):
    name: str
    password_hash: str
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
