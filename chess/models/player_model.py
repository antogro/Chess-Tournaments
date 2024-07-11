from tinydb import TinyDB, Query
from chess.models.data_manager import ManageData
import os

DB_PATH_PLAYER = "_data/players.json"


class Player:
    """
    Permet de sauvegarder le informations des joueurs
    """

    def __init__(self,
                 name,
                 first_name,
                 birth_date,
                 doc_ID,
                 chess_id,
                 rank):

        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.doc_ID = doc_ID
        self.chess_id = chess_id
        self.rank = rank

        self.manage_data = ManageData

        if not os.path.exists('_data'):
            os.mkdir('_data')
        self.db = TinyDB(DB_PATH_PLAYER)
        self.table_player = self.db.table('players')

    def doc_id_player(self, player_data):
        """doc id player"""
        all_player = self.table_player.all()
        highest_doc_id = max([doc.doc_id for doc in all_player]) if all_player else 0
        new_doc_id = highest_doc_id + 1
        player_data["doc_ID"] = new_doc_id

        return player_data

    def get_player_by_id(self, chess_id):
        """Renvoie le joueur par son id"""
        Player = Query()
        player_id = self.table_player.search(Player.doc_ID == chess_id)
        if player_id == []:
            return None
        else:
            return player_id
