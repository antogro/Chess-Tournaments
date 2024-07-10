
# from typing import Dict, Any
from tinydb import TinyDB, Query
import os

from chess.models.data_manager import ManageData
DB_PATH_TOURNAMENT = "_data/tournament.json"
DB_PATH_PLAYER = "_data/players.json"


class TournamentModel:
    def __init__(self,
                 name,
                 place,
                 start_date,
                 end_date,
                 description,
                 player_list,
                 number_of_round):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.player_list = player_list
        self.number_of_round = number_of_round
        self.rounds = 4

        self.manage_data = ManageData

        if not os.path.exists("_data"):
            os.mkdir("_data")
        self.db_tournament = TinyDB(DB_PATH_TOURNAMENT)
        self.table_tournament = self.db_tournament.table("tournament")
        pass

    def get_tournament_data(self):
        return self.table_tournament.all()

    def get_one_tournament_data(self, tournament_name):
        Tournament = Query()
        return self.table_tournament.search(Tournament.name == tournament_name)


class TournamentPlayer:

    def __init__(self):
        self.db = TinyDB(DB_PATH_PLAYER)
        self.db_player = self.db.table('players')
        pass

    def parsed_player_number(self, list_player_number):
        player_number = [int(s) for s in list_player_number.split()]
        return player_number
    
    def choose_player(self, list_player_number, tournament_data):
        """choose player for the tournament"""
        player_list = []
        Player = Query()
        for player_id in list_player_number:
            player = self.db_player.get(Player.doc_ID == int(player_id))
            if player:
                player_list.append(player)
        
            player_list = [{
             'first_name': player['first_name'],
             'last_name': player['last_name'],
             'chess_id': player['chess_id'],
             'rank': player.get('rank', player.get('Rank', 0))
            } for player in player_list]

        return tournament_data, player_list



class TournamentRepport:
    def __init__(self) -> None:
        pass
