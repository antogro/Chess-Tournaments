from chess.views.player_view import PlayerView
from chess.models.player_model import SavePlayer


class PlayerControl:
    def __init__(self, main_controller):
        self.player_view = PlayerView()
        self.player_model = SavePlayer()
        self.main_controller = main_controller

    def manage_player(self):

        while True:
            choice = self.player_view.display_player_menu()

            if choice == "1":
                player_add = self.player_view.add_player()
                self.player_model.add_new_player(player_add)
                self.player_view.display_new_player(player_add)
            elif choice == "2":
                player_list = self.player_model.get_player_list()
                self.player_view.display_player_table(player_list)

            elif choice == "3":
                break
            else:
                self.player_view.display_error_message("Do a better choice")
                continue
