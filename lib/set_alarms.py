# -*- coding: utf-8 -*-

import psycopg2
import os
import datetime

from urllib import parse


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
