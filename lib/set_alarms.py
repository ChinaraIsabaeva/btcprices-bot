# -*- coding: utf-8 -*-

import psycopg2
import os
import datetime

from urllib.parse import urlparse


url = urlparse(os.environ["DATABASE_URL"])


def save_alarms_settings(timestamp, chat_id, alarm_type):
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = connection.cursor()
    cursor.execute(
        "SELECT chat_id from alarms WHERE chat_id={chat_id};".format(
            chat_id=chat_id
        )
    )
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute(
            "INSERT INTO alarms (chat_id, time, alarm_type) SELECT {chat_id}, "
            "'{time}', '{alarm_type}' WHERE NOT EXISTS (SELECT chat_id "
            "FROM alarms WHERE chat_id={chat_id});".format(
                chat_id=chat_id,
                time=datetime.datetime.fromtimestamp(timestamp).isoformat(),
                alarm_type=alarm_type
            )
        )
        if alarm_type == 'daily':
            text = "You alarm was set. Starting tomorrow you will receive " \
                   "prices every day at the beginning of this hour."
        else:
            text = "You alarm was set. Starting next hour you will receive prices at the beginning of every hour."
    else:
        text = "You have active alarm already."
    connection.commit()
    connection.close()
    return text


def delete_alarm_settings(chat_id):
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = connection.cursor()
    cursor.execute("DELETE from alarms WHERE chat_id={chat_id};".format(chat_id=chat_id))
    text = "You alarm has been deleted."
    connection.commit()
    connection.close()
    return text
