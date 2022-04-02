import os
from functools import cache

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if 'DATABASE_URL' in os.environ:
    DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
else:
    DATABASE_URL = 'postgresql://eswan18@localhost/ethan_runs'

Base = declarative_base()


@cache
def get_engine() -> Engine:
    return create_engine(DATABASE_URL)


def get_db():
    engine = get_engine()
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
