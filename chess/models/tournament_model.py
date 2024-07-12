# from typing import Dict, Any
from tinydb import TinyDB, Query
import os


from chess.models.data_manager import ManageData

DB_PATH_TOURNAMENT = "_data/tournament.json"
DB_PATH_PLAYER = "_data/players.json"


class TournamentModel:
    def __init__(
        self,
        name,
        place,
        start_date,
        description,
        number_of_round,
        status="in_progress",
        current_round=1,
        match=None,
    ):
        self._name = name
        self._place = place
        self._start_date = start_date
        self._description = description
        self._number_of_round = number_of_round
        self._status = status
        self._current_round = current_round
        self.match = match if match is not None else []
        self.manage_data = ManageData()

        if not os.path.exists("_data"):
            os.mkdir("_data")
        self.db_tournament = TinyDB(DB_PATH_TOURNAMENT)
        self.table_tournament = self.db_tournament.table("tournament")
        pass

    def tournament_to_dict(self):
        return {
            "name": self._name,
            "place": self._place,
            "start_date": self._start_date,
            "description": self._description,
            "number_of_round": self._number_of_round,
            "current_round": self._current_round,
            "status": self.status,
            "match": self.match,
        }

    @property
    def current_round(self):
        return self._current_round

    @current_round.setter
    def current_round_setter(self, value):
        self._current_round = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status_setter(self, value):
        if value in ["progress", "paused", "finished"]:
            self._status = value
        else:
            raise ValueError("Invalid status")

    def next_round(self):
        self._current_round += 1

    def set_status_in_progress(self):
        self._status = "progress"

    def set_status_paused(self):
        self._status = "paused"

    def set_status_finished(self):
        self._status = "finished"

    def get_tournament_data(self):
        return self.table_tournament.all()

    def save_tournament(self):
        return self.table_tournament.insert(self.tournament_to_dict())

    def get_one_tournament_data(self, tournament_name):
        Tournament = Query()
        return self.table_tournament.search(Tournament.name == tournament_name)


class TournamentPlayer:

    def __init__(self):
        self.db = TinyDB(DB_PATH_PLAYER)
        self.db_player = self.db.table("players")
        self.manage_data = ManageData()
        pass

    def parsed_player_number(self, list_player_number):
        player_number = [int(s) for s in list_player_number.split()]
        return player_number

    def choose_player(self, list_player_number):
        """choose player for the tournament"""
        player_list = []
        for player_id in list_player_number:
            player = self.manage_data.get_player(player_id)
            if player:
                player_list.append(player)

        return player_list


class TournamentRepport:
    def __init__(self) -> None:
        pass
