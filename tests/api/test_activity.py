from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models import User, Activity
from app.schemas.activity import ActivityIn, ActivityOut


# Type alias for the mock data
MockData = dict[str, list[dict[str, Any]]]

BASE_ROUTE = '/activity'

client = TestClient(app)


def test_activity_count_succeeds(mock_db_with_activities: Session):
    n_activities = mock_db_with_activities.query(Activity).count()
    response = client.get(f'{BASE_ROUTE}/count')
    assert response.status_code == 200
    assert response.json() == n_activities


def test_get_activity_fails_unauthenticated() -> None:
    response = client.get(BASE_ROUTE)
    assert response.status_code == 401


def test_post_activity_fails_unauthenticated(mock_data: MockData):
    new_activity = ActivityIn(**mock_data['activities'][0])
    response = client.post(BASE_ROUTE, data=new_activity.json())
    assert response.status_code == 401


def test_post_activity_succeeds(
    authenticated_user: User,
    mock_db: Session,
    mock_data: MockData,
):
    n_activities_before = mock_db.query(Activity).count()
    new_activity = ActivityIn(**mock_data['activities'][0])
    response = client.post(BASE_ROUTE, data=new_activity.json())
    assert response.status_code == 201
    # Make sure the response is a valid activity.
    _ = ActivityOut(**response.json())
    # And that there is an additional record in the db.
    n_activities_after = mock_db.query(Activity).count()
    assert n_activities_after == n_activities_before + 1
