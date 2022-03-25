from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user import UserOut


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
    new_user = UserIn(name='Aragorn', email='strider@gondor.gov', password='anduril')
    response = client.post(BASE_ROUTE, json=new_user)
