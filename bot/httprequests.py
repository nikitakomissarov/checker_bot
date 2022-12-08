import requests
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

class Asks:
    def __init__(self, dm_token, url):
        self.dm_token = dm_token
        self.url = url

    def timehack(self, timestamp, **response):
        while response['status'] != 'found':
            try:
                headers = {"Authorization": self.dm_token, "timestamp": timestamp}
                response = requests.get(self.url, headers=headers).json()
                timestamp = str(response['timestamp_to_request'])
            except ReadTimeout:
                pass
            except ConnectTimeout:
                pass
            except ConnectionError:
                pass
        return response

    def request(self):
        headers = {"Authorization": self.dm_token}
        response = requests.get(self.url, headers=headers).json()
        timestamp = str(response['timestamp_to_request'])
        if response['status'] != 'found':
            response = self.timehack(timestamp, **response)
            return response
        else:
            return response