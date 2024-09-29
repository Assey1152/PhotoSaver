import requests


class YAInterface:
    def __init__(self, token, version='v1'):
        self.base_url = f'https://cloud-api.yandex.net/{version}'
        self.headers = {'Authorization': f'OAuth {token}'}

    def create_folder(self, folder_name):
        url = f'{self.base_url}/disk/resources'
        params = {'path': folder_name}
        response = requests.put(url, headers=self.headers, params=params)
        return response

    def disk_info(self):
        url = f'{self.base_url}/disk'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_load_url(self, path):
        url = f'{self.base_url}/disk/resources/upload'
        params = {'path': path,
                  'overwrite': True
                  }
        response = requests.get(url, params=params, headers=self.headers)
        return response

    def load_to_url(self, upload_link, file):
        response = requests.put(upload_link, files={'file': file})
        return response

    def load_file(self, path, file):
        response = self.get_load_url(path)
        if response.status_code == 200:
            load_url = response.json()['href']
            response = self.load_to_url(load_url, file)
        return response

