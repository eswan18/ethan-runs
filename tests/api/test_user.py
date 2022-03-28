import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user import UserIn, UserOut
from app.models import User


client = TestClient(app)

BASE_ROUTE = '/user'


def test_get_all_users_succeeds_authenticated(authenticated_user):
    '''Fetching users should return a list of users.'''
    response = client.get(BASE_ROUTE)
    assert response.status_code == 200
    raw_result = response.json()
    # We should have received a list of users
    assert isinstance(raw_result, list)
    # Make sure these entities are valid as UserOuts with no additional data.
    _ = [UserOut.parse_obj(obj) for obj in raw_result]


def test_get_all_users_fails_unauthenticated():
    response = client.get(BASE_ROUTE)
    assert response.status_code == 401


def test_get_user_me_succeeds_authenticated(authenticated_user):
    '''Fetching the current user should return a user.'''
    response = client.get(BASE_ROUTE + '/me')
    assert response.status_code == 200


def test_get_user_me_fails_unauthenticated():
    '''Fetching the current user should fail when unauthenticated.'''
    response = client.get(BASE_ROUTE + '/me')
    assert response.status_code == 401


def test_post_user_succeeds(mock_db):
    username, email, pw = 'Aragorn', 'strider@gondor.gov', 'anduril'
    new_user = UserIn(username=username, email=email, password=pw)
    response = client.post(BASE_ROUTE, data=new_user.json())
    assert response.status_code == 201
    assert response.json() == {'username': username, 'email': email}

@pytest.mark.parametrize('collision_field', ['username', 'email'])
def test_post_user_fails_on_repeat_user_or_email(mock_db_with_users, collision_field):
    # Find a user record in the db.
    user = mock_db_with_users.query(User).first()
    # Create a "new" user that has a conflict with a user already in the db.
    fresh_user = {
        'username': 'Aragorn',
        'email': 'strider@gondor.gov',
        'password':'anduril'
    }
    conflicting_user = fresh_user | {collision_field: getattr(user, collision_field)}
    new_user = UserIn(**conflicting_user)
    response = client.post(BASE_ROUTE, data=new_user.json())
    assert response.status_code == 409
