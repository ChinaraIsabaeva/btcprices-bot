import requests


def get_prices():
    message = requests.get('http://btcprices.info/api/latestprice').json()[0]
    data = ''
    for key in message:
        data += key + ': ' + message[key] + '\n'
    return data
