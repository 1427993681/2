from flask import Flask
import datetime
app = Flask(__name__)
@app.route('/')
def home():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Current Time: {current_time}"
if __name__ == '__main__':
    app.run(port=5000, debug=True)
import pytest
@pytest.fixture
def client():
    from my_flask_app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    expected_response = "Current Time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert expected_response in str(response.data)