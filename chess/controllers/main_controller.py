from ..views.menu_view import MenuView
from ..controllers.tournament_controller import TournamentControl
from ..controllers.player_controller import MainPlayerControl
from ..views.base_views import Display


class MainController:
    """Main control of the chess application"""

    def __init__(self):
        self.menu_view = MenuView()
        self.player_controller = MainPlayerControl()
        self.tournament_controller = TournamentControl()
        self.view = Display()

    def run(self):
        """Main loop of the application"""

        while True:
            choice = self.menu_view.application_menu()

            if choice == "1":
                self.tournament_controller.manage_tournament()

            elif choice == "2":
                self.player_controller.manage_player()

            elif choice == "q" or choice == "Q":
                self.view.display_message(
                    "Thank you for using Python chess tournament"
                    )
                break

            else:
                self.view.display_message(
                    "Invalid choice"
                    )
