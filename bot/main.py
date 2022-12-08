import telegram
from httprequests import Asks
from status import Status
from dotenv import dotenv_values

config = dotenv_values('.env')


def main():
    DM_TOKEN = config['DM_TOKEN']
    BOT_TOKEN = config['BOT_TOKEN']
    URL = 'https://dvmn.org/api/long_polling/'

    bot = telegram.Bot(token=BOT_TOKEN)
    chat_id = bot.get_updates()[0]['message']['chat']['id']


    checkstatus = Asks(DM_TOKEN, URL).request()
    Status(chat_id, bot, **checkstatus).sending()


if __name__ == "__main__":
    main()