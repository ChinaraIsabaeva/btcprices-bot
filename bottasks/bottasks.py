import os, json

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route('/getUpdates/', methods=['POST'])
def get_updates():
    try:
        data = json.loads(request)
        print data
        return 'OK'
    except Exception:
        print Exception.message
        


if __name__ == '__main__':
    app.run(debug=True, port='8080')
