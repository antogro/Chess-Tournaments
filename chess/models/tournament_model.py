
# from typing import Dict, Any
from tinydb import TinyDB, Query
import os


DB_PATH_TOURNAMENT = "_data/tournament.json"
DB_PATH_PLAYER = "_data/players.json"


class TournamentModel:
    def __init__(self):
        if not os.path.exists("_data"):
            os.mkdir("_data")
        self.db_tournament = TinyDB(DB_PATH_TOURNAMENT)
        self.table_tournament = self.db_tournament.table("tournament")
        pass

    def add_new_tournament(self, tournament_data):
        self.table_tournament.insert({
            "name": tournament_data["name"],
            "place": tournament_data["place"],
            "start date": tournament_data["start date"],
            "end date": tournament_data["end date"],
            "description": tournament_data["description"],
            "player list": tournament_data["player list"],
            "number of round": tournament_data["number of round"],
        })

    def get_all_tournament_data(self, tournament_data, player_list, number_of_round):
        # current_round
        """get more information for the tournament"""
        tournament_data["player list"] = player_list
        tournament_data["number of round"] = number_of_round

    def get_tournament_data(self):
        return self.table_tournament.all()

    def get_one_tournament_data(self, tournament_name):
        Tournament = Query()
        return self.table_tournament.search(Tournament.name == tournament_name)

    def number_of_round(self, tournament_number_of_round):
        if tournament_number_of_round is None:
            return 4
        else:
            try:
                return int(tournament_number_of_round)
            except ValueError:
                print("The righting number is not available, using default number : 4.")
                return 4


class TournamentPlayer:

    def __init__(self):
        self.db = TinyDB(DB_PATH_PLAYER)
        self.db_player = self.db.table('players')

    def parsed_player_number(self, list_player_number):
        player_number = [int(s) for s in list_player_number.split()]
        return player_number

    def choose_player(self, list_player_number):
        """choose player for the tournament"""
        player_list = []
        Player = Query()
        for player_id in list_player_number:
            player = self.db_player.get(Player.doc_ID == int(player_id))
            if player:
                player_list.append(player)
            else:
                return None
        return player_list


class TournamentRepport:
    def __init__(self) -> None:
        pass
