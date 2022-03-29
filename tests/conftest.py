from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


@pytest.fixture(autouse=True, scope='session')
def _mock_db_connection():
    '''An isolated database for tests.'''
    from app.main import app
    from app.database import get_db, Base
    from app import models
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
    # Clean up the database for next time.
    db.query(models.User).delete()
    db.query(models.Activity).delete()
    db.commit()

@pytest.fixture(autouse=False, scope='function')
def mock_db(_mock_db_connection):
    '''A self-cleaning version of the database for each test.'''
    from app import models
    try:
        yield _mock_db_connection
    finally:
        _mock_db_connection.query(models.User).delete()
        _mock_db_connection.query(models.Activity).delete()
        _mock_db_connection.commit()

@pytest.fixture(autouse=False, scope='function')
def mock_db_with_users(mock_db):
    from app import models
    user1 = models.User(
        username='elrond',
        email='halfelf@rivendell.com',
        pw_hash='1234'
    )
    user2 = models.User(
        username='frodo',
        email='frodo@thewest.com',
        pw_hash='1234'
    )
    mock_db.add(user1)
    mock_db.add(user2)
    mock_db.commit()
    return mock_db


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
