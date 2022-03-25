import os
from configparser import ConfigParser
from uuid import uuid4

import pytest


def pytest_configure(config):
    '''Automatically set the app secret from the config file.'''
    secrets = ConfigParser()
    secrets.read('./secrets.ini')
    app_secret = secrets['DEVELOPMENT']['APP_SECRET']
    os.environ['APP_SECRET'] = app_secret


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
    app.dependency_overrides = {}
