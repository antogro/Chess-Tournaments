from typing import Any
from .table_manager import TableManager
from .._database._database import db_player


class Player:

    table: TableManager = db_player

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        chess_id: str,
        score: float,
        doc_id=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.doc_id = doc_id
        self.score = score

    @property
    def full_name(self):
        """Returne the full name of a player"""
        return f"{self.last_name} {self.first_name}"

    @property
    def to_dict(self):
        """convert a Player object to a dictionary"""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "chess_id": self.chess_id,
            "score": self.score,
            "doc_id": self.doc_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """convert a dictionary to a Player object"""
        return cls(**data)

    def create_player(self, data: dict) -> dict:
        """create and set the doc_id to the new player in the database"""
        all_player = self.table.load_all()
        highest_doc_id = int(max([doc["doc_id"] for doc in all_player])
                             if all_player else 0)
        self.doc_id = highest_doc_id + 1
        data["doc_id"] = self.doc_id
        return data

    def save(self) -> int:
        """save the player to the database"""
        data: dict = self.to_dict
        id = self.table.save(data)
        return id

    @classmethod
    def all(cls) -> list:
        """get all players from the database"""
        return cls.table.load_all()

    @classmethod
    def get_player(cls, id: int) -> "Player":
        """get a player by id from the database"""
        player = cls.table.load_from_id(id)
        return cls.from_dict(player)
