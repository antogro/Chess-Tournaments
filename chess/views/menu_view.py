class MenuView:
    """Main mase menu"""

    def application_menu(self):
        """Display main menu"""
        print("Welcome inside the Chess Application, choose a number. ")
        print("1. Tournament manager")
        print("2. Player manager")
        print("Q. Exit the application")
        print("")
        choice = input("Do your choice: ")

        return choice
