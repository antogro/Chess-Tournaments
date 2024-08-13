class RoundView:

    def manage_round_view(self):
        """select to stop or to start the round"""
        print("Whould you want to start the round ?")
        print("Please select an option:")
        print("1. Start the round")
        print("2. Return to the main menu")
        choice = input("Do a choice: ")
        return choice

    def get_round_choice(self):
        """Select to stop or to continue to write result"""
        print("1. If you want to start to write result")
        print("2. if you want to paused the round.")
        return input("\n Do your choice: ")

    def get_match_result(self, pairing, name):
        """Get the result of one match between 2 players"""
        print(f"\n -- {name}: Player 1: "
              f"{pairing.player1_score.player.full_name} -- ")
        print("VS")
        print(f" -- {name}: Player 2:"
              f" {pairing.player2_score.player.full_name} -- \n")
        while True:
            result = input(
                "write the number of the result "
                "(Player1 win = 1, Player2 win = 2, Draw = 0): "
            )
            if result in ["0", "1", "2"]:
                return result
            else:
                print("\n Invalid input, "
                      "must be 0, 1 or 2. please try again! \n")

    def display_match_result(self, winner_name, is_draw=False):
        """Display the result of one match between 2 players"""
        if is_draw:
            print("\n --- Round is draw --- \n")
        else:
            print(f"\n ---- Winner -> {winner_name} <- ---- \n")
