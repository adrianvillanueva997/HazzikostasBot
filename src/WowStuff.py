import requests
import os
import json


class wow_api:
    def __init__(self):
        self.region = 'us'
        self.realm = 'wyrmrest-accord'
        self.realm_id = '1369'
        self.__token = self.__login()
        self.base_url = 'https://us.api.blizzard.com'

    def __login(self):
        with open('config.json') as file:
            content = file.read()
            config_content = json.loads(content)
        header = {
            'grant_type': 'client_credentials'
        }
        response = requests.post('https://us.battle.net/oauth/token', data=header,
                                 auth=(config_content["client"], config_content["secret"]))
        response_json = response.json()
        return response_json

    def get_character_basic_info(self, name):
        try:
            re = requests.get(
                f'https://us.api.blizzard.com/profile/wow/character/wyrmrest-accord/{name}?access_token={self.__token["access_token"]}&region=us&namespace=profile-us&locale=en_US')
            print(re.json())
            return re.json()
        except Exception as e:
            print(e)
            return None

    def get_character_media(self, name):
        re = requests.get(
            f'https://us.api.blizzard.com/profile/wow/character/wyrmrest-accord/{name}/character-media?access_token={self.__token["access_token"]}&region=us&namespace=profile-us&locale=en_US')
        # print(re.json())
        return re.json()

    def get_character_stats(self, name):
        re = requests.get(
            f'https://us.api.blizzard.com/profile/wow/character/wyrmrest-accord/{name}/statistics?access_token={self.__token["access_token"]}&region=us&namespace=profile-us&locale=en_US')
        print(re.json())
        return re.json()
