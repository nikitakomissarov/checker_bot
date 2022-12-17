import telegram
import requests
from dotenv import dotenv_values
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

config = dotenv_values('.env')

DEVMAN_TOKEN = config['DEVMAN_TOKEN']
TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
URL = 'https://dvmn.org/api/long_polling/'


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    chat_id = bot.get_updates()[0]['message']['chat']['id']
    greet_message = f"The bot's starting, your chat id {chat_id}"
    bot.send_message(text=greet_message, chat_id=chat_id)
    timestamp = None

    while True:
        try:
            headers = {"Authorization": DEVMAN_TOKEN, "timestamp_to_request": timestamp}
            print(headers)
            response = requests.get(URL, headers=headers)
            response.raise_for_status()
            filtered_response = response.json()
            if filtered_response['status'] != 'found':
                timestamp = str(filtered_response['timestamp_to_request'])
                print(timestamp)
            else:
                message = (
                    f'Преподаватель проверил работу {filtered_response["lesson_title"]}, она {"принята." if filtered_response["is_negative"] == "False" else "не принята, исправьте ошибки."} Ссылка на урок: {filtered_response["lesson_url"]}')
                bot.send_message(text=message, chat_id=chat_id)
        except ReadTimeout:
            pass
        except ConnectTimeout:
            pass
        except ConnectionError:
            pass

if __name__ == "__main__":
    main()
