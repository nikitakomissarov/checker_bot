import telegram
from httprequests import request
from dotenv import dotenv_values

config = dotenv_values('.env')

DEVMAN_TOKEN = config['DEVMAN_TOKEN']
TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
URL = 'https://dvmn.org/api/long_polling/'


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    chat_id = bot.get_updates()[0]['message']['chat']['id']
    greet_message = f"The bot's starting, your chat id {chat_id}"
    bot.send_message(text=greet_message, chat_id=chat_id)

    checkstatus = request(DEVMAN_TOKEN, URL)

    message = (
        f'Преподаватель проверил работу {checkstatus["lesson_title"]}, она {"принята." if checkstatus["is_negative"] == "False" else "не принята, исправьте ошибки."} Ссылка на урок: {checkstatus["lesson_url"]}')
    bot.send_message(text=message, chat_id=chat_id)

if __name__ == "__main__":
    main()
