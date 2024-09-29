import sys
import os
import json
import requests
import logging
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime
from VKInterface import VKInterface
from YAInterface import YAInterface

load_dotenv()
access_token = os.getenv('vk_access_token')
yandex_token = os.getenv('yandex_token')


class PhotoSaver:
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            # filename="process_log.log",
                            # filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

    def save_photo(self, user_id, album_id, count):
        vk = VKInterface(access_token)
        user_info = vk.users_info(user_id).json()
        if user_info.get('error'):
            logging.error(f'Failed reading user info: {user_info["error"]}')
            sys.exit()
        logging.info('Received user info')
        user_info = user_info.get('response')[0]
        folder_name = f'{user_info.get("first_name")}_{user_info.get("last_name")}'
        user_photos = vk.photos_get(user_id, album_id, count).json()
        if user_photos.get('error'):
            logging.error(f'Failed load photos info: {user_photos["error"]}')
            sys.exit()
        photo_items = user_photos.get('response').get('items')
        if len(photo_items) == 0:
            logging.warning('No photos to save')
            sys.exit()
        logging.info('Received user photos info')
        photo_list = []
        duplicate_names = []
        for item in photo_items:
            max_size = max(item['sizes'], key=lambda x: x['height'] * x['width'])
            if item['likes']['count'] in duplicate_names:
                photo_name = f'{item["likes"]["count"]}_{datetime.fromtimestamp(item["date"]).date()}.jpg'
            else:
                duplicate_names.append(item['likes']['count'])
                photo_name = f'{item["likes"]["count"]}.jpg'
            photo_list.append([photo_name, max_size['type'], max_size['url'], item['date']])

        ya_disk = YAInterface(yandex_token)
        folder_response = ya_disk.create_folder(folder_name)
        if folder_response.status_code not in [201, 409]:
            logging.error(f'Error creating folder: {folder_response.json()["message"]}')
            sys.exit()
        json_data = []
        for photo in tqdm(photo_list, ncols=100, desc='Loading photos: '):
            photo_path = f'{folder_name}/{photo[0]}'
            response = requests.get(photo[2])
            load_response = ya_disk.load_file(photo_path, response.content)
            if load_response.status_code in [201, 202]:
                json_data.append({'file_name': photo[0],
                                  'size': photo[1]})
                tqdm.write(f'Photo {photo[0]} loaded')
                # logging.info(f'Photo {photo[0]} loaded')
            else:
                tqdm.write(f'Error loading {photo[0]}: {load_response.json()["message"]}')
                # logging.error(f'Error loading {photo[0]}: {load_response.json()["message"]}')
        logging.info('Photos loaded')
        with open("result.json", "w") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        logging.info('Result file saved')
