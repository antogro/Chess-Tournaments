from chess.models.data_manager import ManageData
from chess.views.player_view import PlayerView
from chess.models.player_model import Player, PlayerManager
from chess.models.table_manager import TableManager


class MainPlayerControl:
    def __init__(self):
        self.player_control = PlayersControl()
        self.view = PlayerView()

    def manage_player(self):

        while True:
            choice = self.view.display_player_menu()

            if choice == "1":
                self.player_control.add_player()

            elif choice == "2":
                self.player_control.display_player_list()

            elif choice == "Q" or choice == "q":
                break

            else:
                self.view.display_error_message("Do a better choice")
                continue


class PlayersControl:
    def __init__(self):
        self.manage_data = ManageData()
        self.table_manager = TableManager()
        self.player_manager = PlayerManager()
        self.player_view = PlayerView()

    def add_player(self):
        data = self.player_view.get_player_data()
        player_data = self.player_manager.creat_player(data)
        player = Player(**player_data)
        self.player_manager.save_player(player)
        self.table_manager.display_table("Player list : ", [player.to_dict()])

        self.player_view.display_new_player(player)
        


    def display_player_list(self):
        player_list = self.player_manager.get_player_list()
        self.table_manager.display_table("Player list", [player for player in player_list])
