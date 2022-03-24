from fastapi.testclient import TestClient
from app.main import app
from app.schemas.user import UserOut

client = TestClient(app)

BASE_ROUTE = '/user'

def test_get_all_users():
    '''Fetching users should return a list of users.'''
    response = client.get(BASE_ROUTE)
    assert response.status_code == 200
    raw_result = response.json()
    # We should have received a list of users
    assert isinstance(raw_result, list)
    # TODO: Eventually, should figure out how to make sure these entities are
    # valid as UserOuts.
