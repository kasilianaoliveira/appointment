from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
