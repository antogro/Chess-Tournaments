



def data_player():
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