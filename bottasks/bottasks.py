import os, json

from flask import Flask, request, redirect, url_for

WEBHOOK_URL_PATH = "/getUpdates/%s/" % (os.environ['TOKEN'])
PORT = os.environ['PORT']

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route(WEBHOOK_URL_PATH, methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        data = request.data
        return redirect(url_for('updates'), data)

@app.route('/updates')
def last_updated(data):
    return data
    
        
if __name__ == '__main__':
    app.run(debug=True, port=PORT)
