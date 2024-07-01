from typing import Dict, Any
from tinydb import TinyDB, Query
import os

DB_PATH_PLAYER = "_data/players.json"


class SavePlayer:
    """
    Permet de sauvegarder le informations des joueurs
    """

    def __init__(self):
        if not os.path.exists('_data'):
            os.mkdir('_data')
        self.db = TinyDB(DB_PATH_PLAYER)
        self.table_player = self.db.table('players')

    def add_new_player(self, player_data: Dict[str, Any]):
        """Ajouter un nouveau joueur"""

        self.table_player.insert({
            "first_name": player_data["first_name"],
            "last_name": player_data["last_name"],
            "birth_date": player_data["birth_date"],
            "chess_id": player_data["chess_id"]
             })

    def get_player_list(self):
        """Renvoie la liste des joueurs"""
        return self.table_player.all()

    def get_player_by_id(self, chess_id):
        """Renvoie le joueur par son id"""
        Player = Query()
        return self.table_player.search(Player.chess_id == chess_id)
