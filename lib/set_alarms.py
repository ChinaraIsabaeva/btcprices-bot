# -*- coding: utf-8 -*-

import psycopg2
import os
import datetime

from urllib import parse


TOKEN = os.environ['TOKEN']
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])


def save_alarms_settings(user_id, timestamp, chat_id):
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = connection.cursor()
    time = datetime.datetime.fromtimestamp(timestamp).strftime('%H')
    alarm = int(time)
    try:
        cursor.execute("INSERT INTO alarms (id, chat_id, alarm) SELECT {user_id}, {chat_id}, {alarm} WHERE NOT EXISTS (SELECT id FROM alarms WHERE id={user_id});".format(user_id=user_id, chat_id=chat_id, alarm=alarm))
        text = 'You alarm was set. Starting tomorrow you will receive prices every day at this time.'
    except ValueError:
        text = 'You already set alarm'
    connection.commit()
    connection.close()
    return text
