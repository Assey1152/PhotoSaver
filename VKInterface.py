import requests


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
        return response

    def photos_get(self, owner_id, album_id='profile', count=5):
        url = f'{self.base_url}photos.get'
        params = {
            **self.params,
            'owner_id': owner_id,
            'album_id': album_id,
            'count': count,
            'extended': 1,
            'photo_sizes': 0
        }
        response = requests.get(url, params=params)
        return response
