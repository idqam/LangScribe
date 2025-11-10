import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import QueuePool

load_dotenv()

db_url = URL.create(
    drivername="postgresql+asyncpg",
    username=str(os.getenv("POSTGRES_USER")),
    password=str(os.getenv("POSTGRES_PASSWORD")),
    host=str(os.getenv("POSTGRES_HOST")),
    port=5432,
    database=str(os.getenv("POSTGRES_DB")),
)

engine = create_async_engine(
    db_url,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def transaction() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
