from tinydb import TinyDB
from chess.models.data_manager import ManageData
import os

DB_PATH_PLAYER = "_data/players.json"


class Player:
    """
    Permet de sauvegarder le informations des joueurs
    """

    def __init__(self,
                 last_name,
                 first_name,
                 birth_date,
                 chess_id,
                 doc_id,
                 score=0):

        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.score = score
        self.doc_id = doc_id

        self.manage_data = ManageData()

        if not os.path.exists('_data'):
            os.mkdir('_data')
        self.db = TinyDB(DB_PATH_PLAYER)
        self.table_player = self.db.table('players')

    def player_to_dict(self):
        return {
            'name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'chess_id': self.chess_id,
            'score': self.score,
            'doc_id': self.doc_id
        }
    
    def doc_id_player(self, player_data):
        """doc id player"""
        all_player = self.table_player.all()
        highest_doc_id = max([doc.doc_id for doc in all_player]) if all_player else 0
        new_doc_id = highest_doc_id + 1
        player_data["doc_id"] = new_doc_id
        return player_data

    def save_player(self):
        return self.table_player.insert(self.player_to_dict())

    def set_player_list(self):
        self.player_list = []
        for player in self.table_player.all():
            self.player_list.append(player["name"])
            return self.player_list
        
    def get_player(self, player_id):
        return self.manage_data.get_player(player_id)

    # def get_player_by_id(self, chess_id):
    #     """Renvoie le joueur par son id"""
    #     Player = Query()
    #     player_id = self.table_player.search(Player.doc_ID == chess_id)
    #     if player_id == []:
    #         return None
    #     else:
    #         return player_id
