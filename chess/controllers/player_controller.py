from chess.views.player_view import PlayerView
from chess.models.player_model import Player
from ..views.base_views import Display

class MainPlayerControl:
    def __init__(self):
        self.player_control = PlayersControl()
        self.view = PlayerView()
        self.display = Display()

    def manage_player(self):

        while True:
            choice = self.view.display_player_menu()

            if choice == "1":
                self.player_control.add_player()

            elif choice == "2":
                self.player_control.display_player_list()
            
            elif choice == "3":
                self.player_control.get_player_by_id()

            elif choice == "Q" or choice == "q":

                break

            else:
                self.display.display_error_input()
                continue
  

class PlayersControl(Player):
    def __init__(self):
        self.player_view = PlayerView()
        self.display = Display()
        self.players = Player(self, self, self ,self, self, self)  

    def add_player(self):
        data = self.player_view.get_player_data()
        player = self.create_player(data)
        new_player = Player(**player)

        new_player.save()
        self.display.display_table("New player created: ", [new_player.to_dict])
        self.player_view.display_new_player(new_player)

    def display_player_list(self):
        player = self.players.all()
        self.display.display_table("Player list", player)

    def get_player_by_id(self):
        player = self.players.all()
        self.display.display_table("Player list", player)
        choice = self.display.display_input("Right id of the player to modify: ")
        player_data = self.players.get_player(int(choice))
