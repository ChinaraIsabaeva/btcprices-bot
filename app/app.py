# -*- coding: utf-8 -*-

import os

from flask import Flask, request

from bot.bot import Bot

TOKEN = os.environ['TOKEN']
WEBHOOK_URL_PATH = "/getUpdates/{token}/".format(token=TOKEN)

app = Flask(__name__)

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    bot = Bot(TOKEN)
    if request.method == 'POST':
        print (request.get_json())
        updates = bot.get_update(request.get_json())
        bot.send_message(updates)
        return 'OK'

    
        
if __name__ == '__main__':
    app.run(debug=True)
