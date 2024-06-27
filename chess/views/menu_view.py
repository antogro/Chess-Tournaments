

class MenuView:
    """Main mase menu"""

    def application_menu(self):
        print("Welcome inside the Chess Application, choose a number. ")
        print("1. Tournament controllers")
        print("2. Player controllers")
        print("Q. Exit the application")
        print("")
        choice = input("Do the best choice for you!")

        return choice
        else:
            print("Erreur, veuillez choisir 1 pour rentrer un nouveau utilisateur.")
