from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os


class ToonManagement:
    def __init__(self):
        self.__engine = create_engine(
            f"mysql+mysqldb://{os.getenv('db_username')}:{os.getenv('db_password')}@{os.getenv('db_hostname')}",
            encoding='utf-8')

    def insert_toon(self, toon_name, user_id: str, user_name):
        with self.__engine.connect() as conn:
            query = text('''INSERT INTO Discord_Bots.HK_Toons
                         (Toon_Name, User_ID, UserName)
                        VALUES(:_toon_name, :_user_id, :_username);''')
            try:
                conn.execute(query, _toon_name=toon_name, _user_id=user_id, _username=user_name)
            except Exception as e:
                print(e)
                return -1
        return 0

    def get_toons(self):
        with self.__engine.connect() as conn:
            query = text('''select Toon_Name, UserName, Added from Discord_Bots.HK_Toons''')
            results = conn.execute(query)
            data = {
                'toons': [],
                'usernames': [],
            }
            for result in results:
                data['toons'].append(result['Toon_Name'])
                data['usernames'].append(result['UserName'])
            return data

    def delete_toon(self, toon_name: str):
        with self.__engine.connect() as conn:
            query = text('''delete from Discord_Bots.HK_Toons where Toon_Name = :_toon_name''')
            conn.execute(query, _toon_name=toon_name)
