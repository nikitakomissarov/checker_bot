import telegram
from httprequests import request
from dotenv import dotenv_values
from status import sending

config = dotenv_values('.env')

DEVMAN_TOKEN = config['DEVMAN_TOKEN']
TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
URL = 'https://dvmn.org/api/long_polling/'

def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    chat_id = bot.get_updates()[0]['message']['chat']['id']
    print(f"The bot's starting, your chat id {chat_id}")

    checkstatus = request(DEVMAN_TOKEN, URL)
    sending(bot, chat_id, **checkstatus)


if __name__ == "__main__":
    main()