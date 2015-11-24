from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route('/getUpdates/<token>')
def get_updates():
    return Response(status=200)


if __name__ == '__main__':
    app.run()
