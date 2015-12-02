import os

from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route('/getUpdates/', methods=['GET'])
def get_updates():
    if request.args.get('token') == os.environ['TOKEN']:
        return request
    else:
        "Request is not form Telegram"


if __name__ == '__main__':
    app.run(debug=True)
