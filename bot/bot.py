#!/usr/bin/python

import os
import requests
import json

from lib.prices import get_prices
from lib.set_alarms import save_alarms_settings, delete_alarm_settings


TOKEN = os.environ['TOKEN']
BASE_URL = "https://api.telegram.org/bot{token}/".format(token=TOKEN)
HELP_MSG = "You can find more information at: http://btcprices.info" \
           "\n\nTo get help just send me message with text 'help' or command \n'/help'." \
           "\n\n To get prices send me message with text 'price' or command \n'/price'." \
           "\n\nAlso you can use this bot in inline mode. Use query 'help' to get help and 'price' to get price"


class Bot(object):
    def __init__(self, token):
        self.token = token

    def _post_method(self, method, data):
        try:
            response = requests.post(BASE_URL + method, json=data)
            print(response)
        except Exception as e:
            print(e)
            return 400

    def get_update(self, received_request):
        accepted_fields = ['message', 'edited_message', 'inline_query']
        has_accepted_field = any(
            i in accepted_fields for i in received_request.keys()
        )

        user = None
        chat_id = None

        for k, value in received_request.items():
            if type(value) is dict:
                for key in value:
                    if key == 'from':
                        user = value.get(key)
                    if key == 'chat':
                        chat_id == value.get(key)
        if user:
            chat_id = user.get('id')
        else:
            chat_id = chat_id
        response = dict(
            chat_id=chat_id,
            user=user,
        )

        if has_accepted_field:
            if 'inline_query' in received_request.keys():
                text = "Currently not working"
            else:
                message = received_request.get('message')
                if message is None:
                    message = received_request.get('edited_message')

                text = message.get('text')
                date = message.get('date')
                response.update(date=date)

        else:
            text = "I accept message or inline query only"
        response.update(text=text)

        return response

    def create_text_message(self, response):
        keyboard = [[{
            'text': 'price'},
            {'text': 'set alarm'},
            {'text': 'delete alarm'}
        ], ]
        received_msg = response.get('text')
        if any(
                received_msg.lower() in substr for substr in [
                    'btcprices', 'цена', '/price'
                ]
        ):
            text = get_prices()

        elif received_msg.lower() == 'set alarm':
            text = 'You can set alarm to receive prices daily or hourly.'
            keyboard = [[{'text': 'daily'}, {'text':'hourly'}], ]
        elif received_msg.lower() == 'hourly':
            text = save_alarms_settings(
                response['date'], response['chat_id'], 'hourly'
            )
        elif received_msg.lower() == 'daily':
            text = save_alarms_settings(
                response['date'], response['chat_id'], 'daily'
            )
        elif received_msg.lower() == 'delete alarm':
            text = delete_alarm_settings(response['chat_id'])
        else:
            text = response.get('text')

        message = dict(
            chat_id=response['chat_id'],
            text=text,
            reply_markup=dict(keyboard=keyboard, resize_keyboard=True)
        )
        return message

    def create_inline_message(self, updates):
        if updates['query'] in 'btcprices':
            text = get_prices()
            results = [{'type': 'article', 'title': 'price', 'message_text': text, 'id': updates['id']+'/0'}]
        else:
            results = [{'type': 'article', 'title': 'help', 'message_text': HELP_MSG, 'id': updates['id']+'/0'}]
        return {'inline_query_id': updates['id'], 'results': json.dumps(results)}

    def send_message(self, updates):
        if 'query' in updates.keys():
            inlinedata = self.create_inline_message(updates)
            self._post_method('answerInlineQuery', inlinedata)
            self._post_method('sendMessage', dict(chat_id=645526, text='{0} воспользовался твоим ботом'.format(updates['user'])))
        else:
            data = self.create_text_message(updates)
            print("sending data", data)
            if updates.get('user'):
                first_name = updates.get('user')['first_name']
            else:
                first_name = None
            self._post_method('sendMessage', data)
            self._post_method(
                'sendMessage', dict(
                    chat_id=645526,
                    text='{first_name},{chat_id} воспользовался твоим ботом'.format(
                        first_name=updates.get('user')['first_name'],
                        chat_id=updates.get('chat_id')
                    )
                )
            )
        return 'OK'

    def send_daily_msg(self, chat_id, text):
        self._post_method('sendMessage', dict(chat_id=chat_id, text=text))
        return 'OK'
