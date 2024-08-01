from tinydb import TinyDB
from ..models.table_manager import TableManager


DB_PATH_PLAYER = "_data/players.json"
DB_PATH_TOURNAMENT = "_data/tournament.json"

db = TinyDB(DB_PATH_PLAYER)
db_player = TableManager(db.table("players"))

db = TinyDB(DB_PATH_TOURNAMENT)
db_tournament = TableManager(db.table("tournament"))