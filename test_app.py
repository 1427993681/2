import pytest
from app import app

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert b"Current Time" in response.data
