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

    def chess_id_construc(self, chess_id):
        """construc the chess id code"""

        while True:
            if not chess_id:
                print("N/A")
                return None

            if len(chess_id) != 7:
                print("Invalid ID: must be 7 charactere")
                return None
            chess_id_letter = chess_id[:2]
            chess_id_number = chess_id[2:]

            if not chess_id_letter.isalpha():
                print("Invalid ID: must start by 2 letters")

                return None

            if not chess_id_number.isdigit():
                print("Invalid ID: must end by 5 number")
                return None

            chess_id = f"{chess_id_letter.upper()}{chess_id_number}"
            return chess_id

    def add_new_player(self, player_data: Dict[str, Any]):
        """Ajouter un nouveau joueur"""
        doc_id = self.table_player.insert({
            "first_name": player_data["first_name"],
            "last_name": player_data["last_name"],
            "birth_date": player_data["birth_date"],
            "chess_id": player_data["chess_id"]
            })
        print(doc_id)
        self.table_player.update({"Doc ID": doc_id}, doc_ids=[doc_id])

    def get_player_list(self):
        """Renvoie la liste des joueurs"""
        return self.table_player.all()

    def get_player_by_id(self, chess_id):
        """Renvoie le joueur par son id"""
        Player = Query()
        player_id = self.table_player.search(Player.chess_id == chess_id)
        if player_id == []:
            return None
        else:
            return player_id
