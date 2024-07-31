from dataclasses import dataclass
from typing import Dict, Any
from .table_manager import TableManager
from .._database._database import db_player


class Player:
    table: TableManager = db_player

    def __init__(self, 
                 first_name,
                 last_name, 
                 birth_date, 
                 chess_id, 
                 score,
                 doc_id = None, 
                 ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.doc_id = doc_id
        self.score = score

    def __repr__(self) -> str:
        return f"{self.doc_id}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    @property
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
    def from_dict(cls, data: dict[str, Any]):
        return cls(**data)

    
    def create_player(self, data: dict) -> dict:
        all_player = self.table.load_all()
        highest_doc_id = max([doc.doc_id for doc in all_player]) if all_player else 0
        self.doc_id = int(highest_doc_id) + 1
        data["doc_id"] = self.doc_id
        return data
    
    def save(self) -> int:
        data: dict = self.to_dict
        id = self.table.save(data)
        return id

    @classmethod
    def all(cls) -> list['Player']:
        return cls.table.load_all()
        
    @classmethod
    def get_player(cls, id: int) -> 'Player':
        player = cls.table.load_from_id(id)        
        return cls.from_dict(player) 
