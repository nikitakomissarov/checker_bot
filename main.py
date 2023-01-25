import telegram
import requests
from dotenv import dotenv_values
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError
import time
import logging
from logging.handlers import TimedRotatingFileHandler

config = dotenv_values('.env')

DEVMAN_TOKEN = config['DEVMAN_TOKEN']
TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
CHAT_ID = config['CHAT_ID']
URL = 'https://dvmn.org/api/long_polling/'

greet_message = f"The bot's been started, your chat id {CHAT_ID}"

handler = TimedRotatingFileHandler("app.log", when='D', backupCount=30)
handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(handler_format)
logger.addHandler(handler)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=TELEGRAM_TOKEN)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = None

    logger.info(greet_message)

    while True:
        try:
            headers = {"Authorization": DEVMAN_TOKEN, "timestamp_to_request": timestamp}
            response = requests.get(URL, headers=headers)
            response.raise_for_status()
            lesson_result = response.json()
            if lesson_result['status'] != 'found':
                timestamp = str(lesson_result['timestamp_to_request'])
            else:
                message = (
                    f'Преподаватель проверил работу {lesson_result["lesson_title"]},'
                    f'она {"принята." if lesson_result["is_negative"] == "False" else "не принята, исправьте ошибки."}'
                    f'Ссылка на урок: {lesson_result["lesson_url"]}'
                )
                bot.send_message(text=message, chat_id=CHAT_ID)
        except ReadTimeout:
            pass
        except ConnectTimeout:
            pass
        except ConnectionError:
            time.sleep(5)
            pass


if __name__ == "__main__":
    logger.addHandler(TelegramLogsHandler(CHAT_ID))
    main()
