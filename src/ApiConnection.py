from typing import Tuple

import requests
import logging
import os


class ApiConnection:
    def __init__(self):
        self.__username = os.getenv("api_user")
        self.__code = os.getenv("api_password")
        pass

    @staticmethod
    def get_characters() -> list or None:
        try:
            r = requests.get("https://hazzikostas.thexiao77.xyz/api/v1/characters")
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            print(e)

    @staticmethod
    def get_post_characters() -> list or None:
        try:
            r = requests.get("https://hazzikostas.thexiao77.xyz/api/v1/postcharacters")
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            print(e)

    def register(self, character_name, region, realm) -> Tuple[bool, int]:
        try:
            r = requests.post("https://hazzikostas.thexiao77.xyz/api/v1/createcharacter", params={
                'username': self.__username,
                'password': self.__code,
                'character': character_name,
                'region': region,
                'realm': realm
            })
            if r.status_code == 201:
                return True, r.status_code
            elif r.status_code == 204:
                return False, r.status_code
            return False, r.status_code
        except Exception as e:
            print(e)

    def delete(self, character_name) -> Tuple[bool, int]:
        try:
            r = requests.delete("https://hazzikostas.thexiao77.xyz/api/v1/deletecharacter", params={
                'username': self.__username,
                'password': self.__code,
                'character': character_name,
            })
            if r.status_code == 200:
                return True, r.status_code
            elif r.status_code == 204:
                return False, r.status_code
            return False, r.status_code
        except Exception as e:
            print(e)

    def update_post_status(self, character_name) -> Tuple[bool, int]:
        try:
            r = requests.post("https://hazzikostas.thexiao77.xyz/api/v1/updatecharacter", params={
                'username': self.__username,
                'password': self.__code,
                'character': character_name,
            })
            if r.status_code == 200:
                return True, r.status_code
            return False, r.status_code
        except Exception as e:
            print(e)
