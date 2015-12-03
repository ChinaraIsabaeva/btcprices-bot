# -*- coding: utf-8 -*-

import os
import json
import requests

from flask import Flask, request, redirect, url_for

WEBHOOK_URL_PATH = "/getUpdates/%s/" % (os.environ['TOKEN'])
PORT = int(os.environ['PORT'])

app = Flask(__name__)

@app.route('/')
def home():
    print ("Syasha ne prav")
    return 'Hello chee-bot'

@app.route('/updates/')
def last_updated(data):
    return data

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == 'POST':
        updates = request.get_json()
        chat_id = updates['message']['chat']['id']
        text = ''
        message = {'chat_id': chat_id, 'text': text}
        if updates['message']['text'] == 'price':
            message['text'] = 'Скоро я смогу отправлять цену биткоина в долларах'
        elif updates['message']['text'] in ['привет', 'Привет', 'hi', 'Hi', 'HI', 'hello', 'Hello']:
             message['text'] = 'Привет'
        else:
            message['text'] = 'Я не знаю, что на это сказать'
        requests.post("https://api.telegram.org/bot120560818:AAHKRbbHYEM9l7PIxuW1-3alAGQ1PV0NeUE/sendMessage", json=message)
        return 'OK'

    
        
if __name__ == '__main__':
    app.run(debug=True, port=PORT)
