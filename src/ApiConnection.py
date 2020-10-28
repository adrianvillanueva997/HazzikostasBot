from typing import Tuple

import requests
import logging
import os


class ApiConnection:
    def __init__(self):
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

    @staticmethod
    def register(character_name, region, realm) -> Tuple[bool, int]:
        try:
            r = requests.post("https://hazzikostas.thexiao77.xyz/api/v1/createcharacter", params={
                'username': os.getenv('api_user'),
                'password': os.getenv('api_password'),
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

    @staticmethod
    def delete(character_name) -> Tuple[bool, int]:
        try:
            r = requests.delete("https://hazzikostas.thexiao77.xyz/api/v1/deletecharacter", params={
                'username': os.getenv('api_user'),
                'password': os.getenv('api_password'),
                'character': character_name,
            })
            if r.status_code == 200:
                return True, r.status_code
            elif r.status_code == 204:
                return False, r.status_code
            return False, r.status_code
        except Exception as e:
            print(e)

    @staticmethod
    def update_post_status(character_name) -> Tuple[bool, int]:
        try:
            r = requests.post("https://hazzikostas.thexiao77.xyz/api/v1/updatecharacter", params={
                'username': os.getenv('api_user'),
                'password': os.getenv('api_password'),
                'character': character_name,
            })
            if r.status_code == 200:
                return True, r.status_code
            return False, r.status_code
        except Exception as e:
            print(e)