import requests
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv("vk_access_token")
yandex_token = os.getenv("yandex_token")


class VKInterface:
    def __init__(self, access_token, version='5.131'):
        self.access_token = access_token
        self.version = version
        self.base_url = 'https://api.vk.com/method/'
        self.params = {'access_token': self.access_token, 'v': self.version}

    def users_info(self, users_id):
        url = f'{self.base_url}users.get'
        params = {**self.params, 'user_ids': users_id}
        response = requests.get(url, params=params)
        return response.json()


vk = VKInterface(access_token)
