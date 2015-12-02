import os, json

from flask import Flask, request, Response

WEBHOOK_URL_PATH = "/getUpdates/%s/" % (os.environ['TOKEN'])
PORT = os.environ['PORT']

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route(WEBHOOK_URL_PATH, methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        return request.data
    else:
        return 'It was get request'
        
if __name__ == '__main__':
    app.run(debug=True, port=PORT)
