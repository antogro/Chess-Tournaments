from chess.controllers.round_controller import RoundControl, RoundTournament
from chess.models.data_manager import ManageData
from chess.models.table_manager import TableManager
from chess.views.tournament_view import TournamentsView
from chess.models.tournament_model import TournamentModel, TournamentPlayer
from chess.views.player_view import PlayerView
from chess.models.player_model import Player
from chess.models.round_model import RoundModels
# from chess.views.round_view import RoundView
# from chess.models.player_model import Player


class TournamentControl:
    """fonction to control the tournament"""

    def __init__(self):
        self.tournament_view = TournamentsView()

        self.control_tournament = ControlTournament()

    def manage_tournament(self):
        """manage the tournament"""
        while True:
            choice = self.tournament_view.display_tournament_menu()
            if choice == "1":
                """creat tournament"""
                self.control_tournament.creat_tournament()

            elif choice == "2":
                """Continue the last tournament"""
                self.control_tournament.continue_last_tournament()

            elif choice == "3":
                """select and start round"""
                break
            elif choice == "4":
                """show list of tournament"""
                self.control_tournament.display_tournament()

            elif choice == "5":
                """back to main menu"""

                break
            elif choice == "Q" or choice == "q":
                """exit"""
                break


class ControlTournament:
    """manage the tournament"""

    def __init__(self):
        self.tournament_view = TournamentsView()
        self.tournament_model_player = TournamentPlayer()
        self.player_model = Player(self, self, self, self, self)
        self.data_manager = ManageData()
        self.table_manager = TableManager()
        self.round_model = RoundModels()
        self.player_view = PlayerView(self, self, self, self, self)
        self.round_control = RoundControl(self, self, self)
        self.round_tournament = RoundTournament()
        self.tournament_model = TournamentModel(self, self, self, self, self)

        # self.tournament_model = Tournament()
        pass

    

    def creat_tournament(self):
        """creat tournament"""
        tournament_data = self.tournament_view.get_tournament_data()
        tournament_data = self.tournament_model.doc_id_tournament(tournament_data)
        self.tournament_model = TournamentModel(**tournament_data)

        table_player_list = self.data_manager.get_player_list()

        self.table_manager.display_player_table(table_player_list)
        choice = self.tournament_view.tournament_choose_player()
        player_list = self.tournament_model_player.parsed_player_number(choice)

        tournament_data["player_list"] = player_list

        player_data = self.tournament_model_player.extract_player_list(tournament_data)

        self.player_view.display_number_to_player(player_data)

        tournament_id = self.tournament_model.save_tournament()

        self.table_manager.display_tournament_table(tournament_data)
        self.round_control.round(tournament_data, tournament_id)

    def display_tournament(self):
        """display tournament"""
        tournament_data = self.data_manager.get_tournament_list()
        for tournament in tournament_data:
            self.table_manager.display_tournament_table(tournament)

    def continue_last_tournament(self):
        tournament_id = self.tournament_model.get_last_tournament_id()

        tournament_data = self.tournament_model.resume_tournament(tournament_id)
        print('tournament_data: ', tournament_data)
        self.tournament_model.tournament_to_dict

        self.tournament_model = TournamentModel(**tournament_data)

        self.table_manager.display_tournament_table(tournament_data)
        self.round_control.round(tournament_data, tournament_id)
