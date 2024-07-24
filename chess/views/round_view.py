class RoundView:
    def __init__(self) -> None:
        pass

    def manage_round_view(self):
        print("Whould you want to start the round ?")
        print("Please select an option:")
        print("1. Start the round")
        print("2. Stop  the round")
        print("4. Round report")
        print("5. Return to the main menu")
        choice = input("Do a choice: ")
        return choice

    def get_round_choice(self):
        print("1. If you want to start to write result")
        print("2. if you want to paused the round.")
        return input("\n Do your choice: ")

    def display_pairing(self, pairings):
        print('pairings: ', pairings)
        for pairing in pairings:

            player1 = Player(**pairing['player1'])
            player2 = Player(**pairing['player2'])
            player1_score = pairing['player1_score']
            player2_score = pairing['player2_score']
            print(f"\n -- Player 1: {player1.first_name} {player1.last_name} {player1_score}-- ")
            print("VS")
            print(
                f"\n -- Player 2: {player2.first_name} {player2.last_name} {player2_score}-- \n"
            )

    def get_match_result(self, player1, player2, tournament_data):

        print(
            f"\n -- Round{tournament_data.current_round}: Player 1: {player1} -- "
        )
        print("VS")
        print(
            f" -- Round{tournament_data.current_round}: Player 2: {player2} -- \n"
        )
        while True:
            result = input(
                "write the number of the result (Player1 win = 1, player2 win = 2, draw = 0): "
            )
            if result in ["0", "1", "2"]:
                return result
            else:
                print("\n Invalid input, must be 0, 1 or 2. please try again! \n")

    def display_match_result(self, winner_name, is_draw=False):
        if is_draw:
            print("Round is draw")
        else:
            f"\n ---- {winner_name} win ---- \n"

    def display_round_paused(self):
        print("Round is paused, please select an option:")
