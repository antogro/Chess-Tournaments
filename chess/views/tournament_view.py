from datetime import datetime


class TournamentsView:
    """Show the information of a tournament"""

    def __init__(self):
        pass

    def display_tournament_menu(self):
        """Display the menu of a tournament"""
        print("\n -------Tournament menu-------")
        print("1. Creat a new tournament")
        print("2. creat current tournament report")
        print("3. select and report a tournament")
        print("4. Show the list of tournament")
        print("5. Back to main menu")
        print("Q. Exit")
        print("-------------------------------")

        choice = input("Do your choice: ")

        return choice

    def get_info(self, message):
        return input(message)

    def get_tournament_data(self):
        """
        Get  information for the tournament
        """
        tournament_name = input("Right the name of the tournament: ")
        tournament_place = input("Right the place of the tournament: ")
        tournament_description = input("Right the description of the tournament: ")

        while True:
            tournament_start_date = input(
                "Right the date of the tournament dd/mm/yyyy: "
            )
            if not tournament_start_date:
                start_date = datetime.now().isoformat()
                break
            try:
                start_date = datetime.strptime(tournament_start_date, "%d/%m/%Y")
                break
            except ValueError:
                print("Incorrect data format, should be dd/mm/yyyy")

        number_of_round = self.round_tournament()

        tournament_data = {
            "name": tournament_name,
            "place": tournament_place,
            "start_date": start_date,
            "number_of_round": number_of_round,
            "description": tournament_description,
            "current_round": 1,
            "match": [],
            "status": "in_progress"
        }

        return tournament_data

    def round_tournament(self):
        """Create a round for the tournament"""
        number_of_round = input("Rigth your desire number of round (default:4): ")
        if number_of_round == "":
            return "4"
        else:
            try:
                return int(number_of_round)
            except ValueError:
                print("Incorrect input, Using default value of 4 round")
                return "4"

    def tournament_choose_player(self):
        """fonction to choose a player for a tournament"""

        print("\n ---- choose player by a list----\n")

        choice = input("Do your choice (right number separate by a space): \n")

        return choice

    def tournament_score_menu(self):
        """score for a tournament"""
        print("1 - Right ID of the player to score")
        print("2 - Choose player from the tournament list")
        print("R - Return to the selection menu")
        print("Q - Exit players selection")
        choice = input("Do your choice: ")

        return choice
