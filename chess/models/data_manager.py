from tinydb import TinyDB, Query, where

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
        print('data: ', data)
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
        """Renvoie la liste des tournois"""
        return self.table_tournament.all()

    def load_tournament_data(self, tournament_id):
        result = self.table_tournament.search(where("doc_id") == tournament_id)
        if result is None:
            raise ValueError(f"No tournament find with the id {tournament_id}")
        return result

    def update_tournament(self, tournament_id, update_data):
        self.table_tournament.update(update_data, Query().doc_id == tournament_id)

    def update_player(self, tournament_id, update_data):
        self.table_players.update(update_data, Query().doc_id == tournament_id)

    def get_player(self, player_id):
        return self.table_players.get(Query().doc_id == player_id)

    def get_tournament(self, tournament_id):
        return self.table_tournament.search(Query().doc_id == tournament_id)

    def extract_match_data(self, tournament_data):
        current_round = tournament_data.get("current_round", 1)
        if current_round > 1:
            round_key = f"round {current_round-1}"
        else:
            round_key = f"round {current_round}"

        if "match" not in tournament_data or round_key not in tournament_data["match"]:
            print(f"Aucune donnée de match trouvée pour {round_key}")
            return []

        extracted_data = []
        for round_key, matches in tournament_data["match"].items():
            for match in enumerate(matches):
                extracted_data.append(
                    {
                        "name": f"round {current_round}",
                        "player1": {
                            "score": match["player1"]["score"],
                            "doc_id": match["player1"]["doc_id"],
                        },
                        "player2": {
                            "score": match["player2"]["score"],
                            "doc_id": match["player2"]["doc_id"],
                        },
                        "start_date": match["start_time"],
                        "end_date": match["end_time"],
                    }
                )

        return extracted_data
