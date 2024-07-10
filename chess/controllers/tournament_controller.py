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

    def manage_tournament(self):
        """manage the tournament"""
        while True:
            choice = self.tournament_view.display_tournament_menu()
            if choice == "1":
                """creat tournament"""
                self.control_tournament.creat_tournament()

            elif choice == "2":
                """select and continue tournament"""
                self.control_tournament.display_tournament()

            elif choice == "3":
                """select and start round"""
                self.control_tournament.current_tournament_data()
            elif choice == "4":
                """show list of tournament"""

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
        self.round_view = RoundView()
        pass

    def creat_tournament(self):
        """creat tournament"""
        tournament_data = self.tournament_view.get_tournament_data()
        table_player_list = self.data_manager.get_player_list()
        self.table_manager.display_player_table(table_player_list)
        player_list = self.tournament_view.tournament_choose_player()
        print(player_list)
        parsed_player_list = self.tournament_model_player.parsed_player_number(
            player_list
        )
        print(parsed_player_list)
        tournament_data, player_list = self.tournament_model_player.choose_player(
            parsed_player_list, tournament_data
        )
        print("Type of tournament_data:", type(tournament_data))
        print("Content of player list:", player_list)
        print("Content of tournament_data:", tournament_data)
        tournament_data["player_list"] = player_list
        self.data_manager.save_tournament(tournament_data)
        self.table_manager.display_tournament_table(tournament_data)

    def display_tournament(self):
        """display tournament"""
        tournament_data = self.data_manager.get_tournament_list()
        for tournament in tournament_data:
            self.table_manager.display_tournament_table(tournament)

    def current_tournament_data(self):
        self.display_tournament()
        tournament_name = self.tournament_view.get_info(
            "Right the name of the selected tournament: "
        )
        tournament_data = self.data_manager.load_tournament_data(tournament_name)
        self.table_manager.display_tournament_table(tournament_data)
        round_data = self.round_model.mixed_player(tournament_data)
        print(round_data)
        # round_data = self.round_model.get_versus_player(mixed_player_list)
        round_id = self.data_manager.save_round(round_data)
        self.round_view.manage_round(round_data)
