import os, json

from flask import Flask, request, Response

WEBHOOK_URL_PATH = "/getUpdates/%s/" % (os.environ['TOKEN'])
PORT = os.environ['PORT']

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route(WEBHOOK_URL_PATH, methods=['GET', 'POST'])
def get_updates():
    if request.method == 'POST':
        return Response.data
    else:
        return 'It was ge request'
        
if __name__ == '__main__':
    app.run(debug=True, port=PORT)
