import pytest
from app import app

@pytest.fixture
def client():
    """Create a Flask test client for pytest."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the index dashboard loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"StadiaSync" in response.data

def test_api_status_route(client):
    """Test that the API endpoint returns valid status data."""
    response = client.get('/api/status')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'zones' in data
    assert 'announcement' in data
    assert len(data['zones']) > 0
    assert data['zones'][0]['id'] == 'A'
