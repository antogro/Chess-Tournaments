import random as rd
from datetime import datetime
from chess.models.data_manager import ManageData
from chess.models.table_manager import TableManager
from chess.models.tournament_model import TournamentModel, TournamentPlayer


class RoundModels:
    def __init__(self):
        self.tournament_model_player = TournamentPlayer()
        self.tournament_model = TournamentModel(self, self, self, self, self)
        self.table_manager = TableManager()
        self.data_manager = ManageData()

        pass

    def mixed_player(self, tournament_data):
        if isinstance(tournament_data, list):

            if len(tournament_data) > 0:
                tournament_data = tournament_data[0]

        assert isinstance(tournament_data, dict)
        player_list = tournament_data.get("player_list")
        assert isinstance(player_list, list)

        rd.shuffle(player_list)
        tournament_data["player_list"] = player_list

        return tournament_data

    def creat_pairing_first_round(self, player_data, tournament_data):
        pairings = []
        for i in range(0, len(player_data), 2):
            try:
                player1 = player_data[i]
                player2 = player_data[i + 1]
                pairing = self.creat_match_data(player1, player2, tournament_data)
                pairings.append(pairing)
            except IndexError:
                print("No enought player, one player don't have oppoent")
        return pairings

    def creat_match_data(
        self, player1, player2, tournament_data, start_time=None, end_time=None
    ):

        if start_time is None:
            start_time = datetime.now()
            formated_start_time = start_time.strftime("%d-%m-%Y %H:%M:%S")
        if isinstance(tournament_data, list):
            tournament_data = tournament_data[0] if tournament_data else {}

        return {
            "player1": {
                "doc_id": player1.doc_id,
                "score": player1.score,
                "first_name": player1.first_name,
                "last_name": player1.last_name,
            },
            "player2": {
                "doc_id": player2.doc_id,
                "score": player2.score,
                "first_name": player2.first_name,
                "last_name": player2.last_name,
            },
            "start_time": formated_start_time,
            "end_time": end_time,
        }

    def have_played_before(self, player1, player2, tournament_data):
        if "matches" not in tournament_data:
            return False

        for matche in tournament_data["matches"]:
            if (
                matche["player1"]["doc_id"] == player1["doc_id"]
                and matche["player2"]["doc_id"] == player2["doc_id"]
            ) or (
                matche["player1"]["doc_id"] == player2["doc_id"]
                and matche["player2"]["doc_id"] == player1["doc_id"]
            ):
                return True
        return False

    def creat_pairing_next_round(self, tournament_data):
        player_list = self.tournament_model_player.extract_player_list(tournament_data)
        sorted_players = sorted(player_list, key=lambda x: (-x.score, x.doc_id))
        pairings = []
        used_players = set()

        for i in range(0, len(sorted_players) - 1, 2):
            player1 = sorted_players[i]
            player2 = sorted_players[i + 1]

            if (
                player1.doc_id not in used_players
                and player2.doc_id not in used_players
            ):
                pairing = self.creat_match_data(player1, player2, tournament_data)
                pairings.append(pairing)
                used_players.add(player1.doc_id)
                used_players.add(player2.doc_id)

        # Gérer le cas d'un nombre impair de joueurs
        if len(sorted_players) % 2 != 0:
            last_player = sorted_players[-1]
            if last_player.doc_id not in used_players:
                print(
                    f"Player {last_player.first_name} {last_player.last_name} doesn't have an opponent this round."
                )

        print("pairings: ", pairings)
        return pairings

    def update_tournament_data(self, tournament_data, matches):
        current_round = tournament_data["current_round"]
        round_key = f"round {current_round}"
        if round_key not in tournament_data["match"]:
            tournament_data["match"][round_key] = []

        tournament_data["match"][round_key] = []

        for matche in matches:

            player1 = matche["player1"]
            player2 = matche["player2"]
            matche_result = {
                "player1": {"doc_id": player1["doc_id"], "score": player1["score"]},
                "player2": {"doc_id": player2["doc_id"], "score": player2["score"]},
                "start_time": matche["start_time"],
                "end_time": matche["end_time"],
            }

            tournament_data["match"][round_key].append(matche_result)

        return tournament_data

    def extract_and_display_round(self, tournament_data):
        extract_data = self.data_manager.extract_match_data_from_match(tournament_data)
        extracted_data = self.tournament_model_player.link_player_name(
            tournament_data, extract_data
        )
        self.table_manager.display_round_table(extracted_data)

    def display_pairing_round(self, tournament_data, pairings):
        extracted_data = self.tournament_model_player.link_player_name(
            tournament_data, pairings
        )
        self.table_manager.display_round_table(extracted_data)
