from flask import Flask, render_template_string
import pytest

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('Current Time: {{ current_time }}', current_time='2023-11-30 12:00:00')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_current_time(client):
    response = client.get('/')
    assert 'Current Time' in str(response.data)
    assert '2023-11-30 12:00:00' in str(response.data)

if __name__ == "__main__":
    app.run(debug=True)
运行上面的代码需要在终端中安装 Flask 和 pytest，可以通过执行以下命令来完成：

pip install flask pytest
pytest test_flask_app.py