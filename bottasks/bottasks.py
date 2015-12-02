import os

from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route('/getUpdates/', methods=['GET'])
def get_updates():
    try:
        return ''
    except Exception:
        print Exception.message
        


if __name__ == '__main__':
    app.run(debug=True)
