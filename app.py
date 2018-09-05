# -*- coding: utf-8 -*-

import os

from flask import Flask, request

from bot.bot import Bot

TOKEN = os.environ['TOKEN']
DATABASE_URI = os.environ['DATABASE_URL']
WEBHOOK_URL_PATH = "/getUpdates/{token}/".format(token=TOKEN)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    bot = Bot(TOKEN)
    if request.method == 'POST':
        print(request.get_json())
        updates = bot.get_update(request.get_json())
        bot.send_message(updates)
        return 'OK'


if __name__ == '__main__':
    app.run(debug=True)
