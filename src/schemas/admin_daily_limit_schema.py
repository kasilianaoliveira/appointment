from uuid import UUID

from pydantic import BaseModel

from enums import WeekDay


class AdminDailyLimitCreate(BaseModel):
    week_day: WeekDay
    limit: int


class AdminDailyLimitRead(BaseModel):
    id: UUID
    week_day: WeekDay
    limit: int

    class Config:
        from_attributes = True


class AdminDailyLimitUpdate(BaseModel):
    week_day: WeekDay
    limit: int

    class Config:
        from_attributes = True
