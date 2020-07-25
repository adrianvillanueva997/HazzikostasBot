import requests
import os
import json


class wow_api:
    def __init__(self):
        self.region = 'us'
        self.realm = 'wyrmrest-accord'
        self.realm_id = '1369'
        self.__token = self.__login()

    def __login(self):
        with open('config.json') as file:
            content = file.read()
            config_content = json.loads(content)
        header = {
            'grant_type': 'client_credentials'
        }
        response = requests.post('https://us.battle.net/oauth/token', data=header,
                                 auth=(config_content["client"], config_content["secret"]))
        return response.json()

    def get_character_basic_info(self, name):
        try:
            re = requests.get(
                f'https://us.api.blizzard.com/profile/wow/character/wyrmrest-accord/{name}?access_token={self.__token["access_token"]}&region=us&namespace=profile-us&locale=en_US')
            # print(re.json())
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
        # print(re.json())
        return re.json()


class raider_api:
    def __init__(self):
        self.region = 'us'
        self.realm = 'wyrmrest-accord'
        self.realm_id = '1369'

    def get_affixes(self):
        re = requests.get(
            'https://raider.io/api/v1/mythic-plus/affixes?region=us&locale=en')
        return re.json()

    def get_player_mythic_stats(self, player_name: str):
        re = requests.get(
            f'https://raider.io/api/v1/characters/profile?'
            f'region=us&realm=wyrmrest-accord&name={player_name}&'
            f'fields=mythic_plus_ranks,mythic_plus_recent_runs,mythic_plus_scores_by_season:current')
        # print(re.json())
        return re.json()


if __name__ == '__main__':
    r = raider_api()
    r.get_player_mythic_stats("necrolords")
