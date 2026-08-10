import pytest
from _temp_code import app
import datetime

def test_home():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"Current Time" in response.data
