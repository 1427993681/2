import pytest
from app import app

def test_current_time():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"Current Time" in response.data
