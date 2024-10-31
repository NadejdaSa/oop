import requests
from pprint import pprint
import json
from tqdm import tqdm

def rank_sizes(letter):
    sizes = ['s', 'm', 'x', 'o', 'p', 'q', 'r', 'y', 'z', 'w']
    return sizes.index(letter)


class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.base_address = 'https://api.vk.com/method/'
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
    
    def big_photos_get(self, count=5):
        url = f'{self.base_address}photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'rev' : 1, 'extended': 1, 'count': count}
        response = requests.get(url, params={**self.params, **params})
        
        photo_dict = {}
        photos = [] ##json файл
        
        for photo in tqdm(response.json()['response'] ['items']):
            photo_info = {}
            size = max(photo['sizes'], key=lambda x: rank_sizes(x['type']))
            if photo['likes']['count'] not in photo_dict.keys():
                photo_dict[photo['likes']['count']] = size['url']
                photo_info['file_name'] = f"[photo['likes']['count']].jpg"
            else:
                photo_dict[f"{photo['likes']['count']} + {photo['date']}"] = size['url']
                photo_info['file_name'] = f"{photo['likes']['count']} + {photo['date']}.jpg"
            pass
            photo_info['size'] = size['type']
            photos.append(photo_info)

        with open("photos.json", "w") as file:
            json.dump(photos, file, indent=4)
        
        return photo_dict



class YD:

    def __init__(self, token_yd):
         self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token_yd}'}
         self.base_url = 'https://cloud-api.yandex.net'

    def create_folder(self, folder_name):
        url = f'{self.base_url}/v1/disk/resources'
        params = {'path' : folder_name}
        response = requests.put(url=url, headers=self.headers, params=params)
        return response
    
    def upload(self, file_url, file_name):
        url = f'{self.base_url}/v1/disk/resources/upload'
        params = {'path': f'photovk/{file_name}.png'}
        href = requests.get(url=url, headers=self.headers, params=params).json().get('href')
        data = requests.get(url=file_url)
        requests.put(url=href, data=data, headers=self.headers)        
    


print('Введите id пользователя vk')
user_id = input()

access_token = ''
vk = VK(access_token, user_id)
token_yd = ''

yd = YD(token_yd)
yd.create_folder('photovk')

photo_dict = vk.big_photos_get()
    
for name, photo_url in tqdm(photo_dict.items()):
    yd.upload(photo_url, name)
    pass








