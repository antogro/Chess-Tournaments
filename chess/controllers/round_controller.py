from chess.models.tournament_model import TournamentPlayer
from chess.views.round_view import RoundView
from chess.models.table_manager import TableManager
from chess.models.data_manager import ManageData
from chess.models.round_model import RoundModels


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
                self.round_tournament.first_round_tournament(
                    tournament_data, tournement_id
                )
                continue
            elif choice == "2":
                break


class RoundTournament:
    def __init__(self):
        self.table_manager = TableManager()
        self.data_manager = ManageData()
        self.round_model = RoundModels()
        self.round_view = RoundView()
        self.tournament_model = TournamentPlayer()

    def first_round_tournament(self, tournament_data, tournement_id):
        print("tournement_id: ", tournement_id)

        self.table_manager.display_tournament_table(tournament_data)
        tournament_data = self.round_model.mixed_player(tournament_data)
        list_player_number = tournament_data["player_list"]

        player_list = self.tournament_model.choose_player(list_player_number)

        matches = self.round_view.manage_round(player_list)

        for match in matches:
            for player in player_list:
                if player["doc_id"] == match["player1"]["doc_id"]:
                    player["score"] = match["player1"]["score"]
                elif player["doc_id"] == match["player2"]["doc_id"]:
                    player["score"] = match["player2"]["score"]

        tournament_update = {"player_list": player_list, "match": {"match1": matches}}

        self.data_manager.update_tournament(tournement_id, tournament_update)

    # def second_round_tournament(self, round_id, tournement_data )

    # def manage_round(self, player_list):

    #     if choice == "1":
    #         for i in range(0, len(match), 2):

    #             while True:

    #             if result == "1":
    #                 player1["score"] += 1
    #                 print(
    #                 )
    #             elif result == "2":
    #                 player2["score"] += 1
    #                 print(
    #                     f"\n ---- Player 2: {player2['first_name']} {player2['last_name']} win ---- \n"
    #                 )
    #             elif result == "0":
    #                 print("\n ---- Equality ---- \n")
    #                 player1["score"] += 0.5
    #                 player2["score"] += 0.5
    #             else:
    #                 print("Invalid result")

    #             match["end_time"] = datetime.now().isoformat()

    #     else:
    #         print("Paused")

    #     return matches
