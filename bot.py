import telegram

bot = telegram.Bot('120560818:AAHKRbbHYEM9l7PIxuW1-3alAGQ1PV0NeUE')

def me():
    print bot

def updates():
    updates = bot.getUpdates()
    for item in updates:
        print item.message.text, item.message.chat_id


def main():
    me()
    updates()


if __name__ == '__main__':
    main()
