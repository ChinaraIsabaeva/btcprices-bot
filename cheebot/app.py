# -*- coding: utf-8 -*-

import os
import requests

from flask import Flask, request
from bot import Bot


WEBHOOK_URL_PATH = "/getUpdates/{token}/".format(token=os.environ['TOKEN'])
PORT = int(os.environ['PORT'])

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    bot = Bot(TOKEN)
    if request.method == 'POST':
        print (request.get_json())
        updates = bot.get_update(request.get_json())
        bot.send_message(updates)
        return 'OK'

    
        
if __name__ == '__main__':
    app.run(debug=True, port=PORT)
