import os
from collections.abc import Generator
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from .config import get_db_url

load_dotenv()

db_url = get_db_url()  

print("Creating engine!")

engine = create_engine(
    url='',
    echo=True,
    poolclass=NullPool
)

print("If this doesnt appear ima kms")

SessionLocal = sessionmaker(engine, class_=Session, expire_on_commit=False)


@contextmanager
def transaction() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()