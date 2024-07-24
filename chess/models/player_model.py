from dataclasses import dataclass
from typing import Dict, Any
from tinydb import TinyDB
from chess.models.data_manager import ManageData

DB_PATH_PLAYER = "_data/players.json"


@dataclass
class Player:
    first_name: str
    last_name: str
    birth_date: str
    chess_id: str
    doc_id: int = 1
    score: float = 0.0

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'chess_id': self.chess_id,
            'score': self.score,
            'doc_id': self.doc_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        return cls(**data)


@dataclass
class PlayerManager(ManageData):
    def __init__(self):
        self.manage_data = ManageData()

    def generate_doc_id_player(self, player_data):
        """doc id player"""
        all_player = self.manage_data.get_player_list()
        highest_doc_id = max([doc.doc_id for doc in all_player]) if all_player else 0
        return int(highest_doc_id) + 1
    
    def creat_player(self, player_data):
        self.doc_id = self.generate_doc_id_player(player_data)
        player_data["doc_id"] = self.doc_id
        return player_data
    
    def save_player(self, player: Player):
        return self.manage_data.save_player(player.to_dict())

    def get_player_list(self):
        return self.manage_data.get_player_list()
        
    def get_player(self, player_id: str) -> 'Player':
        player_data = self.manage_data.get_player(player_id)
        if player_data is None:
            raise ValueError(f"No player found for doc id: {player_id}")
        return (player_data)

    # def get_player_by_id(self, chess_id):
    #     """Renvoie le joueur par son id"""
    #     Player = Query()
    #     player_id = self.table_player.search(Player.doc_ID == chess_id)
    #     if player_id == []:
    #         return None
    #     else:
    #         return player_id
