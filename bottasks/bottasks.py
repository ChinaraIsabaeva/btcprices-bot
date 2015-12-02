import os, json

from flask import Flask, request

WEBHOOK_URL_PATH = "/getUpdates/%s/" % (os.environ['TOKEN'])
PORT = os.environ['PORT']

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route(WEBHOOK_URL_PATH, methods=['GET', 'POST'])
def get_updates():
    if request.method == 'POST':
        data = request.get_json(force=True)
        return 'OK'
    else:
        return 'It was ge request'
        
if __name__ == '__main__':
    app.run(debug=True, port=PORT)
