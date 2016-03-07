#!/usr/bin/python

import os
import requests
import json

from lib.prices import get_prices
from lib.set_alarms import save_alarms_settings


TOKEN = os.environ['TOKEN']
BASE_URL = "https://api.telegram.org/bot{token}/".format(token=TOKEN)
HELP_MSG = "You can find more information at: http://btcprices.info\n\nTo get help just send me message with text 'help' or command \n'/help'.\n\n To get prices send me message with text 'price' or command \n'/price'.\n\nAlso you can use this bot in inline mode. Use query 'help' to get help and 'price' to get price\n\n Please rate and review bot at: https://storebot.me/bot/btcprices_bot\n\n"


class Bot(object):
    def __init__(self, token):
        self.token = token

    def _post_method(self, method, data):
        response = requests.post(BASE_URL+method, json=data)
        print(response)

    def get_update(self, received_request):
        if 'inline_query' in received_request.keys():
            inline_query_id = received_request['inline_query']['id']
            query = received_request['inline_query']['query']
            username = received_request['inline_query']['from']['first_name']
            update = dict(id=inline_query_id, query=query, user=username)
        else:
            chat_id = received_request['message']['chat']['id']
            username = received_request['message']['from']['first_name']
            date = received_request['message']['date']
            user_id = received_request['message']['from']['id']
            if 'text' in received_request['message'].keys():
                text = received_request['message']['text']
            else:
                text = ''
            update = dict(chat_id=chat_id, text=text, user=username, date=date, user_id=user_id)
        return update

    def create_text_message(self, updates):
        if updates['text'] != '':
            received_msg = updates['text']
            if any(received_msg.lower() in substr for substr in ['btcprices', 'цена', '/price']):
                text = get_prices()
            elif any(received_msg.lower() in substr for substr in ['/feedback', 'rate and review']):
                text = 'Please rate and leave your review at: https://storebot.me/bot/btcprices_bot'
            elif received_msg.lower() == 'set alarm':
                text = save_alarms_settings(updates['user_id'], updates['date'], updates['chat_id'])
            else:
                text = HELP_MSG
        else:
            text = "I understand only text messages"
        keyboard = [['price', 'help'], ['rate and review', 'set alarm']]
        message = dict(chat_id=updates['chat_id'], text=text, reply_markup=dict(keyboard=keyboard, resize_keyboard=True))
        return message

    def create_inline_message(self, updates):
        text = get_prices()
        if updates['query'] in 'btcprices':
            results = [{'type': 'article', 'title': 'price', 'message_text': text, 'id': updates['id']+'/0'}]
        else:
            results = [{'type': 'article', 'title': 'help', 'message_text': HELP_MSG, 'id': updates['id']+'/0'}]
        return {'inline_query_id': updates['id'], 'results': json.dumps(results)}

    def send_message(self, updates):
        if 'query' in updates.keys():
            print ('In quert if')
            inlinedata = self.create_inline_message(updates)
            print (inlinedata)
            response = self._post_method('answerInlineQuery', inlinedata)
            self._post_method('sendMessage', dict(chat_id=645526, text='{0} воспользовался твоим ботом'.format(updates['user'])))
        else:
            data = self.create_text_message(updates)
            response = self._post_method('sendMessage', data)
            self._post_method('sendMessage', dict(chat_id=645526, text='{0} воспользовался твоим ботом'.format(updates['user'])))
            print ('send message')
        return 'OK'

    def send_daily_msg(self, chat_id, text):
        self._post_method('sendMessage', dict(chat_id=chat_id, text=text))
        return 'OK'
