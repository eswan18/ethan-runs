from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import yaml

from app.main import app
from app.database import get_db, Base
from app.models import User, Activity
from app.auth import get_current_user


SQLALCHEMY_DATABASE_URL = 'postgresql://eswan18@localhost/ethan_runs_test'
MOCK_DATA_FILE = Path(__file__).parent / 'data' / 'mock_data.yaml'


@pytest.fixture(scope='session')
def mock_data():
    with open(MOCK_DATA_FILE, 'rt') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


@pytest.fixture(autouse=True, scope='session')
def _mock_db_connection():
    '''
    An isolated database for tests.

    Not intended for direct use in tests as it doesn't clean up until all tests have
    finished. See the fixture `mock_db` instead for that use case.
    '''
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
    # Clean up the database for next time.
    db.query(User).delete()
    db.query(Activity).delete()
    db.commit()


@pytest.fixture(autouse=False, scope='function')
def mock_db(_mock_db_connection):
    '''A self-cleaning version of the database for each test.'''
    try:
        yield _mock_db_connection
    finally:
        _mock_db_connection.query(User).delete()
        _mock_db_connection.query(Activity).delete()
        _mock_db_connection.commit()


@pytest.fixture(autouse=False, scope='function')
def mock_db_with_users(mock_db, mock_data):
    users = (User(**user) for user in mock_data['users'])
    for user in users:
        mock_db.add(user)
    mock_db.commit()
    return mock_db


@pytest.fixture(autouse=False, scope='function')
def mock_db_with_activities(mock_db, mock_data):
    activities = (Activity(**activity) for activity in mock_data['activities'])
    for activity in activities:
        mock_db.add(activity)
    mock_db.commit()
    return mock_db


@pytest.fixture(scope='function')
def authenticated_user(mock_data):
    # Importing these within the function allows us to set the secrets before
    # the code is run.

    mock_user = User(**mock_data['users'][0])

    async def mock_current_user(token=None, db=None):
        return mock_user

    app.dependency_overrides[get_current_user] = mock_current_user
    # Yielding the object gives tests access to it, for e.g. field comparison.
    yield mock_user
    # Reset the dependencies before moving on to other tests.
    del app.dependency_overrides[get_current_user]
