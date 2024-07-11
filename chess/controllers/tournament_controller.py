from chess.controllers.round_controller import RoundControl, RoundTournament
from chess.models.data_manager import ManageData
from chess.models.table_manager import TableManager
from chess.views.tournament_view import TournamentsView
from chess.models.tournament_model import TournamentModel, TournamentPlayer
from chess.views.player_view import PlayerView
from chess.models.player_model import Player
from chess.models.round_model import RamdomPlayer
from chess.views.round_view import RoundView



class TournamentControl:
    """fonction to control the tournament"""

    def __init__(self):
        self.tournament_view = TournamentsView()
        self.tournament_model = TournamentModel(
            self, self, self, self, self, self, self
        )
        self.tournament_model_player = TournamentPlayer()
        self.player_view = PlayerView()
        self.save_player = Player(self, self, self, self, self, self)
        self.control_tournament = ControlTournament()
        self.round_view = RoundView()

    def manage_tournament(self):
        """manage the tournament"""
        while True:
            choice = self.tournament_view.display_tournament_menu()
            if choice == "1":
                """creat tournament"""
                self.control_tournament.creat_tournament()
                

            elif choice == "2":
                """select and continue tournament"""

            elif choice == "3":
                """select and start round"""
                self.control_tournament.current_tournament_data()

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
        self.tournament_model = TournamentModel(
            self, self, self, self, self, self, self
        )
        self.tournament_model_player = TournamentPlayer()
        self.player_view = PlayerView()
        self.save_player = Player(self, self, self, self, self, self)
        self.data_manager = ManageData()
        self.table_manager = TableManager()
        self.round_model = RamdomPlayer()
        self.round_control = RoundControl(self, self, self)
        self.round_tournament = RoundTournament()
        pass

    def creat_tournament(self):
        """creat tournament"""
        tournament_data = self.tournament_view.get_tournament_data()
        table_player_list = self.data_manager.get_player_list()
        self.table_manager.display_player_table(table_player_list)
        choice = self.tournament_view.tournament_choose_player()
        parsed_player_list = self.tournament_model_player.parsed_player_number(choice        )
        player_list = self.tournament_model_player.choose_player(parsed_player_list)

        tournament_data["player_list"] = player_list

        tournament_id = self.data_manager.save_tournament(tournament_data)
        self.table_manager.display_tournament_table(tournament_data)
        self.round_control.round(tournament_data, tournament_id)

    def display_tournament(self):
        """display tournament"""
        tournament_data = self.data_manager.get_tournament_list()
        for tournament in tournament_data:
            self.table_manager.display_tournament_table(tournament)

    # def current_tournament_data(self):
        
