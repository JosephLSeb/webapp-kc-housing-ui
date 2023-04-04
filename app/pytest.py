import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>Home Page</title>' in response.data

def test_analysis_page(client):
    response = client.post('/analysis', data=dict(bedrooms='3', price_range='1'))
    assert response.status_code == 200
    assert b'<title>Analysis Page</title>' in response.data

def test_invalid_page(client):
    response = client.get('/invalid')
    assert response.status_code == 404