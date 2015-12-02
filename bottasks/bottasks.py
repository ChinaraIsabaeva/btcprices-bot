import os

from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route('/getUpdates/', methods=['GET', 'POST'])
def get_updates():
    if request.args.post('token') == os.environ['TOKEN']:
        return ''
    else:
        "Request is not form Telegram"


if __name__ == '__main__':
    app.run(debug=True)
