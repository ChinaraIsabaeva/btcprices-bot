import os

from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route('/getUpdates/', methods=['POST'])
def get_updates():
    return ''


if __name__ == '__main__':
    app.run(debug=True)
