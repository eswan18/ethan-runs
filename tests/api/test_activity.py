from fastapi.testclient import TestClient

from app.main import app
from app.models import Activity


client = TestClient(app)

BASE_ROUTE = '/activity'


def test_activity_count_succeeds(mock_db_with_activities):
    n_activities = mock_db_with_activities.query(Activity).count()

    response = client.get(f'{BASE_ROUTE}/count')
    assert response.status_code == 200
    assert response.json() == n_activities
