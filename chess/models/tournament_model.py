import os
from typing import Dict, Any
from tinydb import TinyDB, Query


DB_PATH_TOURNAMENT = "_data/tournament.json"


class TournamentModel:
    def __init__(self) -> None:
        if not os.path.exists("_data"):
            os.mkdir("_data")
        self.db_tournament = TinyDB(DB_PATH_TOURNAMENT)
        self.table_tournament = self.db_tournament.table("tournament")
        pass

    def add_new_tournament(self, tournament_data: Dict[str, Any]):
        self.table_tournament.insert(tournament_data)

    def get_tournament_data(self):
        return self.table_tournament.all()

    def get_one_tournament_data(self, tournament_name):
        Tournament = Query()
        return self.table_tournament.search(Tournament.name == tournament_name)


    def creat_tournament(self):
        if tournament_date:
            tournament_start_date, tournament_end_date = tournament_date

        try:
            tournament_number_of_round = int(input("Right the number of round: "))
        except ValueError:
            tournament_number_of_round = 4

class TournamentRepport:
    def __init__(self) -> None:
