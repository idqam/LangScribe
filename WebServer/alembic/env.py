import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path
import os

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from WebServer.resources import get_db_url



config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

#alembic is safer on non async drivers
sync_db_url = get_db_url(async_driver=False)
config.set_main_option("sqlalchemy.url", str(sync_db_url))


target_metadata = None


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()




if context.is_offline_mode():
    run_migrations_offline()