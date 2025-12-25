from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, field_serializer


class ServiceCreate(BaseModel):
    name: str
    description: str
    price: float


class ServiceRead(BaseModel):
    id: UUID
    name: str
    description: str
    price: Decimal
    created_at: datetime
    updated_at: datetime

    @field_serializer("price")
    @staticmethod
    def serialize_price(value: Decimal) -> str:
        quantized = value.quantize(Decimal("0.01"))
        return f"{quantized:.2f}"

    class Config:
        from_attributes = True


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
