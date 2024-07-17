from datetime import datetime
from chess.models.tournament_model import TournamentModel, TournamentPlayer
from chess.views.round_view import RoundView
from chess.models.table_manager import TableManager
from chess.models.data_manager import ManageData
from chess.models.round_model import RoundModels
from chess.views.player_view import PlayerView


class RoundControl:
    def __init__(self, round_number, round_time_start, round_time_end):
        self.round_number = round_number
        self.round_time_start = round_time_start
        self.round_time_end = round_time_end

        self.table_manager = TableManager()
        self.data_manager = ManageData()
        self.round_model = RoundModels()
        self.round_tournament = RoundTournament()
        self.round_view = RoundView()

    def round(self, tournament_data, tournement_id):

        while True:
            choice = self.round_view.manage_round_view()
            if choice == "1":
                self.round_tournament.manage_round(tournament_data, tournement_id)
                continue
            elif choice == "2":
                break

            elif choice == "3":
                break


class RoundTournament:
    def __init__(self):
        self.table_manager = TableManager()

        self.data_manager = ManageData()
        self.round_model = RoundModels()
        self.round_view = RoundView()
        self.player_view = PlayerView(self, self, self, self, self)
        self.tournament_model_player = TournamentPlayer()

    def manage_round(self, tournament_data, tournament_id):
        self.table_manager.display_tournament_table(tournament_data)
        tournament_data = self.round_model.mixed_player(tournament_data)
        player_data = self.tournament_model_player.extract_player_list(tournament_data)

        if tournament_data["current_round"] == 1:
            pairings = self.round_model.creat_pairing_first_round(
                player_data, tournament_data
            )
        else:
            pairings = self.round_model.creat_pairing_next_round(tournament_data)

        self.round_model.display_pairing_round(tournament_data, pairings)

        choice = self.round_view.get_round_choice()

        if choice == "1":
            update_pairings = self.manage_score(pairings, tournament_data)
            tournament_data = self.round_model.update_tournament_data(
                tournament_data, update_pairings
            )
            self.tournament_model = TournamentModel(**tournament_data)
            tournament_data["current_round"] += 1
            self.tournament_model.update_tournament()
            self.round_model.extract_and_display_round(tournament_data)

        else:
            self.round_view.display_round_paused()
            tournament_data = self.round_model.update_tournament_data(
                tournament_data, pairings
            )
            self.tournament_model = TournamentModel(**tournament_data)
            self.tournament_model.paused_tournament(tournament_id)

        if self.tournament_model.current_round >= int(
            tournament_data["number_of_round"]
        ):
            print("match finish")

    def manage_score(self, pairings, tournament_data):
        for pairing in pairings:
            player1 = pairing["player1"]
            player2 = pairing["player2"]

            result = self.round_view.get_match_result(player1, player2, tournament_data)
            player1["score"] = float(player1.get("score", 0))
            player2["score"] = float(player2.get("score", 0))

            if result == "1":
                player1["score"] += 1
                self.round_view.display_match_result(player1["first_name"])
            elif result == "2":
                player2["score"] += 1
                self.round_view.display_match_result(player2["first_name"])
            elif result == "0":
                self.round_view.display_match_result(None, is_draw=True)
                player1["score"] += 0.5
                player2["score"] += 0.5
            player1["score"] = str(player1["score"])
            player2["score"] = str(player2["score"])

            pairing["end_time"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        return pairings
