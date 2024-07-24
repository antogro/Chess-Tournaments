from chess.controllers.round_controller import RoundControl, RoundTournament
from chess.models.data_manager import ManageData
from chess.models.table_manager import TableManager
from chess.views.tournament_view import TournamentsView
from chess.models.tournament_model import TournamentModel, TournamentPlayer, TournamentManager, TournamentPlayerManager
from chess.views.player_view import PlayerView
from chess.models.player_model import Player, PlayerManager
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
                self.control_tournament.select_and_start_round()
                break
            elif choice == "4":
                """show list of tournament"""
                self.control_tournament.display_all_tournament()

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
        self.player_manager = PlayerManager()
        self.tournament_manager = TournamentManager()
        self.table_manager = TableManager()
        self.player_view = PlayerView()
        self.round_control = RoundControl()
        self.round_tournament = RoundTournament()
        self.tournament_player_manager = TournamentPlayerManager()


        # self.tournament_model = Tournament()
        pass



    def creat_tournament(self):
        """creat tournament"""
        tournament_data = self.tournament_view.get_tournament_data()
        tournament = TournamentModel(**tournament_data)

        players = self.player_manager.get_player_list()
        self.table_manager.display_table("Player list", [player for player in players])

        choice = self.tournament_view.tournament_choose_player()
        tournament = self.tournament_player_manager.add_player(choice, tournament)

        player_data = self.tournament_player_manager.extract_player_list(tournament.to_dict)
   
        tournament_id = self.tournament_manager.save_tournament(tournament)

        self.table_manager.display_table("Tournament: ", [tournament.to_dict])
        self.table_manager.display_table("Player list: ", [TournamentPlayer.to_dict(player) for player in player_data])
        print('tournament: ', tournament)
        self.round_control.round(tournament, tournament_id, player_data)

    def display_all_tournament(self):
        """display tournament"""
        tournaments = self.tournament_manager.get_all_tournament()
        self.table_manager.display_table("Tournament", [tournament for tournament in tournaments])

    def continue_last_tournament(self):
        tournament_id = self.tournament_manager.get_last_tournament_id()
        tournament = self.tournament_manager.get_tournament(tournament_id)
        player_data = self.tournament_player_manager.extract_player_list(tournament)
        self.table_manager.display_table("Tournament: ", [tournament.to_dict])
        self.round_control.round(tournament, tournament_id, player_data)

    def select_and_start_round(self):
        """select and start round"""

