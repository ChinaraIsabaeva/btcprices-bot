import os
import requests

TOKEN = os.environ['TOKEN']
BASE_URL = "https://api.telegram.org/bot{token}/".format(token=TOKEN)


class Bot(object):
    def __init__(self, token):
        self.token = token
    
    def _post_method(self, method=None, data=None):
        response = requests.post(BASE_URL+method, json=data)
        return response.status_code


    def send_message(self, data):
        response = _post_method(method='sendMessage', data=data)
        return response.status_code
