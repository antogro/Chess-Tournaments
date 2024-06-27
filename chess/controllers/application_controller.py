from chess.views.menu_view import MenuView
from chess.controllers.tournaments_controller import
from chess.controllers.player_controller import


class ApplicationController:
    """Main control of the chess application"""
    
    def __init__(self):
        self.menu_view = MenuView()
        self.menu_view.application_menu()
        pass

    def run(self):
        """Main loop of the application"""
        exit = False

        while not exit:
            choice = self.menu_view

            if choice == '1':
                self.chess_tournament.tournament()
                break

            elif choice == '2':
                self.add_player()   
                break

            elif choice == 'q' or choice == 'Q':
                exit = True
                break
