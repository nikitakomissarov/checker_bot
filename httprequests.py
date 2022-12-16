import requests
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

def request(devman_token, url, timestamp=None):
    while True:
        try:
            headers = {"Authorization": devman_token, "timestamp_to_request": timestamp}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            filtered_response = response.json()
            if filtered_response['status'] != 'found':
                timestamp = str(filtered_response['timestamp_to_request'])
            else:
                return filtered_response
        except ReadTimeout:
            pass
        except ConnectTimeout:
            pass
        except ConnectionError:
            pass
