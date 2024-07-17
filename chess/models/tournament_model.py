# from typing import Dict, Any
from datetime import datetime
from tinydb import TinyDB, Query
from chess.models.player_model import Player
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
        end_date=None,
        match=None,
        doc_id=None,
        player_list=None,
    ):
        self._name = name
        self._place = place
        self._start_date = start_date
        self._end_date = end_date
        self._description = description
        self._number_of_round = number_of_round
        self._status = status
        self._current_round = current_round
        self._player_list = player_list
        self.doc_id = doc_id
        self.match = match if match is not None else {}
        self.manage_data = ManageData()

        if not os.path.exists("_data"):
            os.mkdir("_data")
        self.db_tournament = TinyDB(DB_PATH_TOURNAMENT)
        self.table_tournament = self.db_tournament.table("tournament")
        pass

    @property
    def tournament_to_dict(self):
        return {
            "doc_id": self.doc_id,
            "name": self._name,
            "place": self._place,
            "start_date": self._start_date,
            "end_date": self._end_date,
            "description": self._description,
            "number_of_round": self._number_of_round,
            "current_round": self._current_round,
            "status": self._status,
            "player_list": self._player_list,
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

    @property
    def number_of_round(self):
        return self._number_of_round

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

    def get_all_tournament_data(self):
        return self.table_tournament.all()

    def get_tournament_data(self, tournament_id):
        return self.manage_data.load_tournament_data(tournament_id)

    def save_tournament(self):
        return self.table_tournament.insert(self.tournament_to_dict)

    def get_tournament_data_by_name(self, tournament_name):
        Tournament = Query()
        return self.table_tournament.search(Tournament.name == tournament_name)

    def update_tournament(self):
        return self.table_tournament.update(self.tournament_to_dict)

    def resume_tournament(self, tournament_id):
        data = self.get_tournament_data(tournament_id)
        if data:
            if isinstance(data, list) and len(data) > 0:
                data = data[0]

            self.doc_id = tournament_id
            self.set_status_in_progress()
        return data

    def paused_tournament(self, tournament_id):
        self.get_tournament_data(tournament_id)
        self.set_status_paused()
        self.update_tournament()

    def complete_tournament(self, tournament_id, tournament_data):
        self.get_tournament_data(tournament_id)
        self.set_status_finished()
        tournament_data["end_date"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.update_tournament()

    def get_last_tournament_id(self):
        all_tournament = self.table_tournament.all()
        if not all_tournament:
            raise ValueError("No tournament_found.")
        return max([doc.doc_id for doc in all_tournament])

    def doc_id_tournament(self, tournament_data):
        """doc id player"""
        all_tournament = self.table_tournament.all()
        highest_doc_id = (
            max([doc.doc_id for doc in all_tournament]) if all_tournament else 0
        )
        new_doc_id = highest_doc_id + 1
        tournament_data["doc_id"] = new_doc_id
        return tournament_data


class TournamentPlayer:

    def __init__(self):
        self.db = TinyDB(DB_PATH_PLAYER)
        self.player_model = Player(self, self, self, self, self)
        self.db_player = self.db.table("players")
        self.manage_data = ManageData()
        pass

    def parsed_player_number(self, list_player_number):
        player_number = [int(s) for s in list_player_number.split()]
        return player_number

    def extract_player_list(self, tournament_data):
        """choose player for the tournament"""
        try:
            list_player_number = tournament_data["player_list"]
            player_list = []
            for player_id in list_player_number:
                player = self.manage_data.get_player(player_id)
                if player:
                    player_list.append(player)

            player_object = []
            for player_data in player_list:
                player_data = Player(
                    first_name=player_data["first_name"],
                    last_name=player_data["last_name"],
                    doc_id=player_data["doc_id"],
                    score=player_data["score"],
                    birth_date=player_data["birth_date"],
                    chess_id=player_data["chess_id"],
                )
                player_object.append(player_data)

            return player_object
        except KeyError:
            raise ValueError("tournament_data must contain a 'player_list' key")

    def link_player_name(self, tournament_data, extracted_matches):
        try:
            player_ids = tournament_data.get("player_list", [])
            player_details = [
                self.manage_data.get_player(player_id) for player_id in player_ids
            ]

            player_dict = {
                player["doc_id"]: f"{player['first_name']} {player['last_name']}"
                for player in player_details
            }

            for match in extracted_matches:
                match["player1"]["name"] = player_dict.get(
                    match["player1"]["doc_id"], "Unknown"
                )
                match["player2"]["name"] = player_dict.get(
                    match["player2"]["doc_id"], "Unknown"
                )
            return extracted_matches

        except KeyError as e:
            print(f"KeyError: {e}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

        # list_player_number = tournament_data["player_list"]
        # player = []
        # for pid in list_player_number:
        #     player_data = self.manage_data.get_player(pid)
        #     if player_data:
        #         player.append(Player(**player_data))

        # return player
        # player_list = []
        # for player_id in list_player_number:
        #     if player:
        #         player_list.append(player)

        # player_object = []
        # for player_data in player_list:
        #     player_data = Player(
        #         first_name=player_data["first_name"],
        #         last_name=player_data["last_name"],
        #         doc_id=player_data["doc_id"],
        #         score=player_data["score"],
        #         birth_date=player_data["birth_date"],
        #         chess_id=player_data["chess_id"],
        #     )
        #     player_object.append(player_data)

        # return player_object


class TournamentRepport:
    def __init__(self) -> None:
        pass
