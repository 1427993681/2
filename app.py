from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"<h1>Current Time: {now}</h1>"

if __name__ == '__main__':
    app.run()
