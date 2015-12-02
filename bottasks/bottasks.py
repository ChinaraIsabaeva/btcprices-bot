import os, json

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route('/getUpdates/', methods=['POST'])
def get_updates():
    try:
        data = request.get_data()
        return data
    except Exception:
        print Exception.message
        


if __name__ == '__main__':
    app.run(debug=True, port='8080')
