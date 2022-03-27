import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if 'DATABASE_URL' in os.environ:
    DATABASE_URL = os.environ['DATABASE_URL']
else:
    DATABASE_URL = 'postgresql://eswan18@localhost/ethan_runs'
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
