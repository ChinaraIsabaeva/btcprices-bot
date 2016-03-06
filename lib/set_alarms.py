import psycopg2, os, datetime, json

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


def save_alarms_settings(timestamp, chat_id):
    cursor = connection.cursor()
    time = datetime.datetime.fromtimestamp(timestamp).strftime('%H')
    alarm = int(time)
    cursor.execute("INSERT INTO alarms (chat_id, alarm) VALUES (%s, %s)", (chat_id, alarm))
    connection.commit()
    connection.close()
    

def send_prices_by_alert():
    print ('send prices alert is working')
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT chat_id, alarm FROM alarms;")
    query = json.dumps(cursor.fetchall(), cls=MyEncoder)
    data = json.loads(query)
    current_hour = datetime.datetime.now().time().hour
    bot = Bot(TOKEN)
    connection.close()
    if current_hour == data[0]['alarm']:
        print ('if stetment is fine')
        chat_id = data[0]['chat_id']
        text = get_prices()
        bot.send_daily_msg(chat_id, text)

def main():
    send_prices_by_alert()

if __name__ == '__main__':
    main()
