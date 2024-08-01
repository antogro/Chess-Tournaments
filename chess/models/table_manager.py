from typing import Union
from tinydb import Query


class TableManager:

    def __init__(self, table):
        self.table = table

    def save(self, data: dict) -> int:
        id = self.table.insert(data)
        return id

    def load_all(self) -> list:
        """Renvoie la liste des tournois"""
        return self.table.all()

    def update(self, data: dict, doc_id: Union[list, int]) -> int:
        return self.table.update(data, Query().doc_id == doc_id)

    def load_from_id(self, doc_id) -> dict:
        return self.table.get(doc_id=doc_id)
    
    def insert_multiple(self, data: list[dict]) -> list[int]:
        return self.table.insert(data)


   