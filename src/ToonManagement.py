from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os


class ToonManagement:
    """
    Public class that does all the character management stuff
    """

    def __init__(self):
        """
        Class constructor
        """
        self.__engine = create_engine(
            f"mysql+mysqldb://{os.getenv('db_username')}:{os.getenv('db_password')}@{os.getenv('db_hostname')}",
            encoding='utf-8')

    def insert_toon(self, toon_name: str, user_id: str, user_name: str):
        """
        Function that receives a toon name, user_id and username, the toon name is given from the command arg
        and the user_id and user_name are received from Discord's api
        :param toon_name:
        :param user_id:
        :param user_name:
        :return:
        """
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

    def get_toons_names(self):
        """
        Public function that gets the toons names from the database
        Returns a dictionary with toons and the username of the user that registered the toon.
        :return:
        """
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
        """
        Public function that deletes everything from certain user in the database
        :param toon_name:
        :return:
        """
        with self.__engine.connect() as conn:
            query = text('''delete from Discord_Bots.HK_Toons where Toon_Name = :_toon_name''')
            conn.execute(query, _toon_name=toon_name)

    def get_toons_full_data(self):
        """
        Function to get all the relevant stats from all characters registered in the database.
        Returns a dictionary with the info
        :return:
        """
        with self.__engine.connect() as conn:
            query = text('''select Toon_Name, _all, dps, tank, healer, tank,
             spec_0, spec_1, spec_2, spec_3, rank_overall,rank_class,rank_faction from Discord_Bots.HK_Toons''')
            results = conn.execute(query)
            data = {
                'toons': [],
                'all': [],
                'dps': [],
                'healer': [],
                'tank': [],
                'spec_0': [],
                'spec_1': [],
                'spec_2': [],
                'spec_3': [],
                'overall': [],
                'class': [],
                'faction': []
            }
            for result in results:
                data['toons'].append(result['Toon_Name'])
                data['all'].append(result['_all'])
                data['dps'].append(result['dps'])
                data['healer'].append(result['healer'])
                data['tank'].append(result['tank'])
                data['spec_0'].append(result['spec_0'])
                data['spec_1'].append(result['spec_1'])
                data['spec_2'].append(result['spec_2'])
                data['spec_3'].append(result['spec_3'])
                data['overall'].append(result['rank_overall'])
                data['class'].append(result['rank_class'])
                data['faction'].append(result['rank_faction'])
            return data

    def update_toon_info(self, toon_name: str, all: float, dps: float, healer: float, tank: float, spec_0: float,
                         spec_1: float, spec_2: float, spec_3: float,
                         rank_overall: float, rank_class: float, rank_faction: float):
        """
        Public function that receives stats from the character and updates all its values from the database.
        :param toon_name:
        :param all:
        :param dps:
        :param healer:
        :param tank:
        :param spec_0:
        :param spec_1:
        :param spec_2:
        :param spec_3:
        :param rank_overall:
        :param rank_class:
        :param rank_faction:
        :return:
        """
        with self.__engine.connect() as conn:
            query = text('''
            UPDATE Discord_Bots.HK_Toons
            SET 
                `_all`=:_all, dps=:_dps, healer=:_healer, tank=:_tank, spec_0=:_spec_0,
                spec_1=:_spec_1, spec_2=:_spec_2, spec_3=:_spec_3, rank_overall=:_rank_overall,
                rank_class=:_rank_class,rank_faction=:_rank_faction
            WHERE 
                Toon_Name = :_toon_name''')
            conn.execute(query, _toon_name=toon_name, _all=all, _dps=dps, _healer=healer, _tank=tank
                         , _spec_0=spec_0, _spec_1=spec_1, _spec_2=spec_2, _spec_3=spec_3,
                         _rank_overall=rank_overall, _rank_faction=rank_faction, _rank_class=rank_class)
