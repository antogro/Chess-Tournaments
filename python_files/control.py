import python_files.chess_tournament as chess_tournament


def main():
    while True:
        print("1. Add a player")
        print("2. Start a tournament")
        print("3. Show the ranking")
        print("4. Exit")
        choice = input('')

        if choice == '1':
            player_data = chess_tournament.data_player()
            save_player = chess_tournament.SavePlayer(player_data)
            save_player.save_new_player()
            break

        elif choice == '2':
            chess_tournament.tournament()
            break

        elif choice == '3':

            break

        elif choice == '4':
            exit()

        else:
            print("Erreur, veuillez choisir 1 pour rentrer un nouveau utilisateur.")
