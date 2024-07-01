from chess.views.menu_view import MenuView
# from chess.controllers.tournament_controller import
from chess.controllers.player_controller import PlayerControl


class MainController:
    """Main control of the chess application"""

    def __init__(self):
        self.menu_view = MenuView()
        self.player_controller = PlayerControl(self)

    def run(self):
        """Main loop of the application"""

        while True:
            choice = self.menu_view.application_menu()

            if choice == '1':
                # self.chess_tournament.tournament()
                print('not implemented yet')

            elif choice == '2':
                self.player_controller.manage_player()

            elif choice == 'q' or choice == 'Q':
                print("Thank you for using Python chess tournament")
                break

            else:
                print("Invalid choice")
