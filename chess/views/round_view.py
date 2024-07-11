class RoundView:
    def __init__(self) -> None:
        pass

    def manage_round_view(
        self,
    ):
        print("Whould you want to start the round ?")
        print("Please select an option:")
        print("1. Start the round")
        print("2. Stop  the round")
        print("3. End the tournament")
        print("4. Round report")
        print("5. Return to the main menu")
        choice = input("Do a choice: ")
        return choice

    def manage_round(self, round_data):
        match = round_data.get("match")
        for i in range(0, len(match), 2):
            try:
                player1 = match[i]
                player2 = match[i + 1]
                print(f"Player 1: {player1['first_name']} {player1['last_name']}")
                print("VS")
                print(f"Player 2: {player2['first_name']} {player2['last_name']}\n")

                result = input("write the number of the result: ")

                if result == "1":
                    player1["rank"] += 1
                    print(
                        f"\n ---- Player 1: {player1['first_name']} {player1['last_name']} win ---- \n"
                    )
                elif result == "2":
                    player2["rank"] += 1
                    print(
                        f"\n ---- Player 2: {player2['first_name']} {player2['last_name']} win ---- \n"
                    )
                elif result == "0":
                    print("\n ---- Equality ---- \n")
                    player1["rank"] += 0.5
                    player2["rank"] += 0.5
                else:
                    print("Invalid result")

            except IndexError:
                print("No match find, or incomplet value")
        print(match)
        return result
