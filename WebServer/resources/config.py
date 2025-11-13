import os

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


def get_db_url(async_driver: bool = True) -> URL:
    """Get database URL with appropriate driver."""
    driver = "postgresql+asyncpg" if async_driver else "postgresql+psycopg2"
    query = {"ssl": "require"} if async_driver else {"sslmode": "require"}

    return URL.create(
        drivername=driver,
        username=str(os.getenv("POSTGRES_USER")),
        password=str(os.getenv("POSTGRES_PASSWORD")),
        host=str(os.getenv("POSTGRES_HOST")),
        port=os.getenv("POSTGRES_PORT"),
        database=str(os.getenv("POSTGRES_DB")),
        query=query,
    )
