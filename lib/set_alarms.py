import psycopg2, os, datetime

from urllib import parse

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

connection = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cursor = connection.cursor()

def save_alarms_settings(timestamp, chat_id):
    time = datetime.datetime.fromtimestamp(timestanp).strftime('%H')
    alarm = int(time)
    cursor.execute("INSERT INTO alarms (chat_id, alarm) VALUES (%s, %s)", (chat_id, alarm))
    connection.commit()
    
