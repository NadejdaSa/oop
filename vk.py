import requests
from pprint import pprint
import json


class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.base_address = 'https://api.vk.com/method/'
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}


    def users_info(self):
        url = f'{self.base_address}users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()
    
    def big_photos_get(self, count = 1):
        url = f'{self.base_address}photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'rev' : 1, 'extended': 1, 'count': 1}
        response = requests.get(url, params={**self.params, **params})
        ##for photo in response.json()
        return response.json()



class YD:

    def __init__(self, token_yd):
         self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token_yd}'}
         self.base_url = 'https://cloud-api.yandex.net'

    def create_folder(self, folder_name):
        url = f'{self.base_url}/v1/disk/resources'
        params = {'path' : folder_name}
        response = requests.put(url=url, headers=self.headers, params=params)
        return response
    
    def upload(self, file_url):
        url = f'{self.base_url}/v1/disk/resources/upload'
        params = {'path': 'photosvk/milana.png'}
        href = requests.get(url=url, headers=self.headers, params=params).json().get('href')
        data = requests.get(url=file_url)
        requests.put(url=href, data=data, headers=self.headers)        
    




access_token = ''
user_id = ''
vk = VK(access_token, user_id)
token_yd = ''
yd = YD(token_yd)
##yd.create_folder('photovk')
pprint(vk.big_photos_get())

##yd.upload(photo)




