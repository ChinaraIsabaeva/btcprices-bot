import requests


def get_prices():
    message = requests.get('http://btcprices.info/api/latestprice').json()
    data = 'BTC prices on ' + message.pop('date') + ':\n'
    for key in message:
        data += key + ': ' + message[key] + '\n'
    return data
