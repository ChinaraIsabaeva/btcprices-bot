# -*- coding: utf-8 -*-

import psycopg2, os, datetime, json
import sys

from urllib import parse
from psycopg2.extras import RealDictCursor

from bot.bot import Bot

from lib.json_encoder import MyEncoder
from lib.prices import get_prices


TOKEN = os.environ['TOKEN']
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

connection = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


def save_alarms_settings(user_id, timestamp, chat_id):
    cursor = connection.cursor()
    time = datetime.datetime.fromtimestamp(timestamp).strftime('%H')
    alarm = int(time)
    cursor.execute("INSERT INTO alarms (id, chat_id, alarm) SELECT {user_id}, {chat_id}, {alarm} WHERE NOT EXISTS (SELECT id FROM alarms WHERE id={user_id});".format(user_id=user_id, chat_id=chat_id, alarm=alarm))
    connection.commit()
    connection.close()
    

def send_prices_by_alert():
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT chat_id, alarm FROM alarms;")
    query = json.dumps(cursor.fetchall(), cls=MyEncoder)
    data = json.loads(query)
    current_hour = datetime.datetime.now().time().hour
    bot = Bot(TOKEN)
    connection.close()
    for row in data:
        if current_hour == row['alarm']:
            print ('if stetment is fine')
            chat_id = row['chat_id']
            text = get_prices()
            bot.send_daily_msg(chat_id, text)

def main():
    send_prices_by_alert()

if __name__ == '__main__':
    main()
