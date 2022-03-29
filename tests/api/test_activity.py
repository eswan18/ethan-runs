from fastapi.testclient import TestClient

from app.main import app
from app.models import Activity
from app.schemas.activity import ActivityIn, ActivityOut


client = TestClient(app)

BASE_ROUTE = '/activity'


def test_activity_count_succeeds(mock_db_with_activities):
    n_activities = mock_db_with_activities.query(Activity).count()
    response = client.get(f'{BASE_ROUTE}/count')
    assert response.status_code == 200
    assert response.json() == n_activities


def test_get_activity_fails_unauthenticated():
    response = client.get(BASE_ROUTE)
    assert response.status_code == 401


def test_post_activity_fails_unauthenticated(mock_data):
    new_activity = ActivityIn(**mock_data['activities'][0])
    response = client.post(BASE_ROUTE, data=new_activity.json())
    assert response.status_code == 401


def test_post_activity_succeeds(authenticated_user, mock_db, mock_data):
    n_activities_before = mock_db.query(Activity).count()
    new_activity = ActivityIn(**mock_data['activities'][0])
    response = client.post(BASE_ROUTE, data=new_activity.json())
    assert response.status_code == 201
    activity = ActivityOut(**response.json())
    n_activities_after = mock_db.query(Activity).count()
    assert n_activities_after == n_activities_before + 1
