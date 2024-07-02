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
                while True:
                    chess_id = self.player_model.chess_id_construc(self.player_view.get_chess_id())
                    if chess_id is not None:
                        break

                player_add = self.player_view.add_player(chess_id)
                self.player_model.add_new_player(player_add)
                self.player_view.display_new_player(player_add)

            elif choice == "2":
                player_list = self.player_model.get_player_list()
                self.player_view.display_player_table(player_list)

            elif choice == "3":
                player_id = self.player_view.get_chess_id()
                player = self.player_model.get_player_by_id(player_id)

                if player is not None:
                    self.player_view.display_player_table(player)
                else:
                    self.player_view.display_error_message(f" No player found with the chess ID : {player_id}")
            elif choice == "4":
                break

            else:
                self.player_view.display_error_message("Do a better choice")
                continue
