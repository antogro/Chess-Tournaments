




class PlayerView():
    def __init__(self) -> None:
        pass

    def select_player_menu():
        print("1. Create a new player")
        print("2. Players list")
        print("3. Exit")
        menu_player = input(int("Right your choose number: "))

        return menu_player


    def add_player(self):
        first_name = input("Rentrer votre nom: ")
        second_name = input("Rentrer votre prénom: ")
        date_birth = input("Rentrer votre date de naissance: ")
        chess_ID = input("Rentrer votre ID de jeu: ")

        player_data = {
            "first_name": first_name,
            "second_name": second_name,
            "Date_birth": date_birth,
            "chess_id": chess_ID
            #"player point":
        }
        return player_data
    
