import telegram
import requests
from dotenv import dotenv_values
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from textwrap import dedent

config = dotenv_values('.env')

DEVMAN_TOKEN = config['DEVMAN_TOKEN']
TG_TOKEN = config['TELEGRAM_TOKEN']
TG_CHAT_ID = config['TG_CHAT_ID']
URL = 'https://dvmn.org/api/long_polling/'
GREET_MESSAGE = f"The bot's been started, your chat id {TG_CHAT_ID}"

logger_info = logging.getLogger('loggerinfo')
logger_error = logging.getLogger("loggererror")
handler = TimedRotatingFileHandler("app.log", when='D', backupCount=30)
handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    bot = telegram.Bot(token=TG_TOKEN)
    timestamp = None
    handler.setFormatter(handler_format)

    logger_info.setLevel(logging.INFO)
    logger_info.addHandler(handler)
    logger_info.addHandler(TelegramLogsHandler(TG_CHAT_ID))

    logger_error.setLevel(logging.ERROR)
    logger_error.addHandler(handler)
    logger_error.addHandler(TelegramLogsHandler(TG_CHAT_ID))

    while True:
        try:
            headers = {"Authorization": DEVMAN_TOKEN, "timestamp_to_request": timestamp}
            response = requests.get(URL, headers=headers)
            response.raise_for_status()
            lesson_result = response.json()
            logger_info.info(f'Структура ответа: {lesson_result}')
            if lesson_result['status'] != 'found':
                timestamp = str(lesson_result['timestamp_to_request'])
            else:
                message = repr(dedent(f''' Преподаватель проверил работу {lesson_result["lesson_title"]},\
 она {"принята." if lesson_result["is_negative"] == "False" 
 else "не принята, исправьте ошибки."}\
 Ссылка на урок: {lesson_result["lesson_url"]}\ '''))
                bot.send_message(text=message, chat_id=TG_CHAT_ID)
        except (ReadTimeout, ConnectionError, Exception) as err:
            logger_error.exception(err)
        except ConnectTimeout as err:
            logger_error.exception(err)
            time.sleep(5)

class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=TG_TOKEN)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)

if __name__ == "__main__":
    main()

