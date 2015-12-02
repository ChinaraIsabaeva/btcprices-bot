import os, json

from flask import Flask, request


WEBHOOK_URL_PATH = "/getUpdates/%s/" % (os.environ['TOKEN'])
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def get_updates():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = request.get_data()
        return ''
    else:
        return 'something was wrong'
        


if __name__ == '__main__':
    app.run(debug=True, port='8443')
