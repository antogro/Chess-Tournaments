from chess.models.data_manager import ManageData
from chess.views.player_view import PlayerView
from chess.models.player_model import Player
from chess.models.table_manager import TableManager


class MainPlayerControl:
    def __init__(self):
        self.player_view = PlayerView()
        self.player_model = Player(self, self, self, self, self, self)
        self.player_control = PlayersControl()

    def manage_player(self):

        while True:
            choice = self.player_view.display_player_menu()

            if choice == "1":
                self.player_control.add_player()

            elif choice == "2":
                self.player_control.display_player_list()

            elif choice == "3":
                

                if player is not None:
                    self.player_view.display_player_table(player)
                else:
                    self.player_view.display_error_message(f" No player found with the chess ID : {player_id}")
            elif choice == "4":
                break

            else:
                self.player_view.display_error_message("Do a better choice")
                continue


class PlayersControl:
    def __init__(self, ):
        self.player_model = Player(self, self, self, self, self, self)
        self.manage_data = ManageData()
        self.player_view = PlayerView()
        self.table_manager = TableManager()

    def add_player(self):
        data = self.player_view.get_player_data()
        player_data = self.player_model.doc_id_player(data)
        self.manage_data.save_player(player_data)
        self.player_view.display_new_player(player_data)

    def display_player_list(self):
        player_list = self.manage_data.get_player_list()
        print(player_list)
        self.table_manager.display_player_table(player_list)
