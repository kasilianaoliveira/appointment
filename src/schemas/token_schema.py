from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
