import os
from configparser import ConfigParser
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


def pytest_configure(config):
    '''Automatically set the app secret from the config file.'''
    secrets = ConfigParser()
    secrets.read('./secrets.ini')
    app_secret = secrets['DEVELOPMENT']['APP_SECRET']
    os.environ['APP_SECRET'] = app_secret


@pytest.fixture(autouse=True, scope='session')
def mock_db():
    '''Use a separate database for tests.'''
    from app.main import app
    from app.database import get_db, Base
    SQLALCHEMY_DATABASE_URL = 'postgresql://eswan18@localhost/ethan_runs_test'
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield db
    # Reset the dependencies before moving on to other tests.
    del app.dependency_overrides[get_db]


@pytest.fixture(scope='function')
def authenticated_user():
    # Importing these within the function allows us to set the secrets before
    # the code is run.
    from app.main import app
    from app.auth import get_current_user
    from app import models
    mock_user = models.User(
        id=uuid4(),
        username='bbaggins',
        email='bilbo@theshire.net',
        pw_hash='1234'
    )

    async def mock_current_user(token=None, db=None):
        return mock_user

    app.dependency_overrides[get_current_user] = mock_current_user
    # Yielding the object gives tests access to it, for e.g. field comparison.
    yield mock_user
    # Reset the dependencies before moving on to other tests.
    del app.dependency_overrides[get_current_user]
