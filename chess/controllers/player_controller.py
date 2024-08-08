from chess.views.player_view import PlayerView
from chess.models.player_model import Player
from ..views.base_views import Display


class MainPlayerControl:
    """Main Class to manager a player"""

    def __init__(self):
        self.player_control = PlayersControl()
        self.view = PlayerView()
        self.display = Display()

    def manage_player(self):
        """Manage the player menu"""
        while True:
            choice = self.view.display_player_menu()

            if choice == "1":
                self.player_control.add_player()

            elif choice == "2":
                self.player_control.display_player_list()

            elif choice.upper() == "Q":
                break

            else:
                self.display.display_error_input()
                continue


class PlayersControl(Player):
    """Class to manage players"""

    def __init__(self):
        self.player_view = PlayerView()
        self.display = Display()

    def add_player(self):
        """Get information and add a player to the database"""
        data = self.player_view.get_player_data()
        player = self.create_player(data)
        new_player = Player(**player)

        new_player.save()
        self.display.display_table("New player created: ",
                                   [new_player.to_dict])
        self.player_view.display_new_player(new_player)

    def display_player_list(self):
        """Display all players from the database"""
        player = Player.all()
        player = sorted(player, key=lambda x: x["last_name"])
        self.display.display_table(
            "Player list (Alphabetic order)",
            player,
            exclude_headers=["score", "birth_date"],
        )
