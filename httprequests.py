import requests
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

negative_message = ('Your task is not checked yet, continue....')
positive_message = ('Your task is checked!')

def timehack(devman_token, url, timestamp, **response_json):
    while response_json['status'] != 'found':
        print(negative_message)
        try:
            headers = {"Authorization": devman_token, "timestamp_to_request": timestamp}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            print(response_json)
            timestamp = str(response_json['timestamp_to_request'])
        except ReadTimeout:
            pass
        except ConnectTimeout:
            pass
        except ConnectionError:
            pass
    print("Your task is checked!")
    return response_json

def request(devman_token, url):
    headers = {"Authorization": devman_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    print(response_json)
    if response_json['status'] != 'found':
        timestamp = str(response_json['timestamp_to_request'])
        response_json = timehack(devman_token, url, timestamp, **response_json)
        return response_json
    else:
        print(positive_message)
        return response_json
