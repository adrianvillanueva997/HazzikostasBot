import requests
import json


class wow_api:
    """
    Public class that connects to the official Blizzard API
    """

    def __init__(self):
        """
        Class constructor
        TODO: Maybe add support for other realms
        """
        self.region = 'us'
        self.realm = 'wyrmrest-accord'
        self.realm_id = '1369'
        self.__token = self.__login()

    def __login(self):
        """
        Private function that logs in the Blizzard's API and gets the login token that is needed to get information
        from the API

        :return:
        """
        with open('config.json') as file:
            content = file.read()
            config_content = json.loads(content)
        header = {
            'grant_type': 'client_credentials'
        }
        response = requests.post('https://us.battle.net/oauth/token', data=header,
                                 auth=(config_content["client"], config_content["secret"]))
        return response.json()

    def get_character_basic_info(self, name: str):
        """
        Public function that receives a character name and returns a dictionary with the basic information.
        :param name:
        :return:
        """
        try:
            re = requests.get(
                f'https://us.api.blizzard.com/profile/wow/character/wyrmrest-accord/{name}?access_token={self.__token["access_token"]}&region=us&namespace=profile-us&locale=en_US')
            return re.json()
        except Exception as e:
            print(e)
            return None

    def get_character_media(self, name: str):
        """
        Public function that receives a character name and returns a dictionary with the media information.
        :param name:
        :return:
        """
        re = requests.get(
            f'https://us.api.blizzard.com/profile/wow/character/wyrmrest-accord/{name}/character-media?access_token={self.__token["access_token"]}&region=us&namespace=profile-us&locale=en_US')
        return re.json()

    def get_character_stats(self, name: str):
        """

        :param name:
        :return:
        """
        re = requests.get(
            f'https://us.api.blizzard.com/profile/wow/character/wyrmrest-accord/{name}/statistics?access_token={self.__token["access_token"]}&region=us&namespace=profile-us&locale=en_US')
        return re.json()


class raider_api:
    """
    Public class that connects to raider.io API
    """

    def __init__(self):
        """
        Class constructor
        """
        self.region = 'us'
        self.realm = 'wyrmrest-accord'
        self.realm_id = '1369'

    def get_affixes(self):
        """
        Public function that receives the weekly affixes, returns a dictionary with the data
        :return:
        """
        re = requests.get(f'https://raider.io/api/v1/mythic-plus/affixes?region={self.region}&locale=en')
        return re.json()

    def get_player_mythic_stats(self, player_name: str):
        """
        Public function that receives a character name and gets the information from it. Currently it gets:
            * Mythic ranks
            * Mythic recent runs
            * Mythic scores in the current season
        :param player_name:
        :return:
        """
        re = requests.get(
            f'https://raider.io/api/v1/characters/profile?'
            f'region=us&realm={self.realm}&name={player_name}&'
            f'fields=mythic_plus_ranks,mythic_plus_recent_runs,mythic_plus_scores_by_season:current')
        return re.json()
