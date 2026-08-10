from flask import Flask, render_template_string
app = Flask(__name__)
@app.route('/')
def current_time():
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now
if __name__ == '__main__':
    app.run(debug=True)
import requests
from pip._internal import main as pip_install
pip_install(['pytest', 'requests'])
def test_current_time():
    response = requests.get('http://127.0.0.1:5000/')
    assert response.status_code == 200
    assert "Current time" in response.text
if __name__ == '__main__':