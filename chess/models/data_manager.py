from tinydb import TinyDB, Query

DB_PATH_PLAYER = "_data/players.json"
DB_PATH_TOURNAMENT = "_data/tournament.json"


class ManageData:
    def __init__(self):
        self.player_db = TinyDB(DB_PATH_PLAYER)
        self.tournament_db = TinyDB(DB_PATH_TOURNAMENT)
        self.table_players = self.player_db.table("players")
        self.table_tournament = self.tournament_db.table("tournament")
        self.table_round = self.tournament_db.table("round")

    def save_player(self, data):
        id = self.table_players.insert(data)
        return id

    def save_tournament(self, tournament_data):
        id = self.table_tournament.insert(tournament_data)
        return id

    def save_round(self, data):
        id = self.table_round.insert(data)
        return id

    def get_player_list(self):
        """Renvoie la liste des joueurs"""
        return self.table_players.all()

    def get_tournament_list(self):
        """Renvoie la liste des joueurs"""
        return self.table_tournament.all()

    def load_tournament_data(self, tournament_name):
        tournament = Query()
        return self.table_tournament.search(tournament.name.search(tournament_name))

    def update_tournament(self, tournament_id, update_data):
        self.table_tournament.update(update_data, Query().doc_id == tournament_id)

    def update_player(self, tournament_id, update_data):
        self.table_players.update(update_data, Query().doc_id == tournament_id)

    def get_player(self, player_id):
        return self.table_players.get(Query().doc_id == player_id)

    def get_tournament(self, tournament_id):
        return self.table_tournament.get(Query().doc_id == tournament_id)

    def update_round(self, round_id, update_data):
        self.table_round.update(update_data, Query().doc_id == round_id)
