from chess.views.tournament_view import TournamentsView
from chess.models.tournament_model import TournamentModel, TournamentPlayer
from chess.views.player_view import PlayerView
from chess.models.player_model import SavePlayer


class TournamentControl:
    """fonction to control the tournament"""
    def __init__(self):
        self.tournament_view = TournamentsView()
        self.tournament_model = TournamentModel()
        self.tournament_model_player = TournamentPlayer()
        self.player_view = PlayerView()
        self.save_player = SavePlayer()

    def manage_tournament(self):
        """manage the tournament"""
        while True:
            choice = self.tournament_view.display_tournament_menu()
            if choice == "1":
                """creat tournament"""
                tournament_data = self.tournament_view.get_tournament_data()

                number_of_round = self.tournament_view.round_tournament()
                round_number = self.tournament_model.number_of_round(number_of_round)

                player_table = self.save_player.get_player_list()

                self.player_view.display_player_table(player_table)
                player_list_str = self.tournament_view.tournament_choose_player()
                player_ids = self.tournament_model_player.parsed_player_number(player_list_str)
                selected_player = self.tournament_model_player.choose_player(player_ids)

                tournament_data = self.tournament_model.get_all_tournament_data(tournament_data, selected_player, round_number)
                print("Type of tournament_data:", type(tournament_data))
                print("Content of tournament_data:", tournament_data)
                self.tournament_model.add_new_tournament(tournament_data)
                self.tournament_view.display_tournament_table(tournament_data)
            elif choice == "2":
                """Creat current tournament report"""

            elif choice == "3":
                """select and report tournament"""

            elif choice == "4":
                """show list of tournament"""

            elif choice == "5":
                """back to main menu"""

                break
            elif choice == "Q" or choice == "q":
                """exit"""
