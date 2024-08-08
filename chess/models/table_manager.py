from tinydb import Query


class TableManager:
    """Class to manage data from and to the data base"""

    def __init__(self, table):
        self.table = table

    def save(self, data: dict) -> int:
        """Save data in the data base"""
        id = self.table.insert(data)
        return id

    def load_all(self) -> list:
        """return a list from the data base"""
        return self.table.all()

    def update(self, data: dict, doc_id: int) -> int:
        """Update data in the data base"""
        return self.table.update(data, Query().doc_id == doc_id)

    def load_from_id(self, doc_id: int) -> dict:
        """Search and load data with an ID from the data base"""
        return self.table.get(doc_id=doc_id)
