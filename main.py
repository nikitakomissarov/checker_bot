import telegram
import requests
from dotenv import dotenv_values
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError
import time

config = dotenv_values('.env')

DEVMAN_TOKEN = config['DEVMAN_TOKEN']
TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
CHAT_ID = config['CHAT_ID']
URL = 'https://dvmn.org/api/long_polling/'

def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    greet_message = f"The bot's starting, your chat id {CHAT_ID}"
    bot.send_message(text=greet_message, chat_id=CHAT_ID)
    timestamp = None

    while True:
        try:
            headers = {"Authorization": DEVMAN_TOKEN, "timestamp_to_request": timestamp}
            response = requests.get(URL, headers=headers)
            response.raise_for_status()
            response_dict = response.json()
            if response_dict['status'] != 'found':
                timestamp = str(response_dict['timestamp_to_request'])
            else:
                message = (
                    f'Преподаватель проверил работу {response_dict["lesson_title"]},'
                    f'она {"принята." if response_dict["is_negative"] == "False" else "не принята, исправьте ошибки."}'
                    f'Ссылка на урок: {response_dict["lesson_url"]}'
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
    main()
