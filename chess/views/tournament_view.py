# from chess.controllers.main_controller import


class TournamentsView:
    """Show the information of a tournament"""

    def display_current_tournament_data(self, tournament_data):
        """Display all the information of a tournament"""
        print(f'Tournament name : {tournament_data["name"]}')
        print(f'Tournament place : {tournament_data["place"]}')
        print(f'Tournament date : {tournament_data["date"]}')
        print(f'Tournament number of rounds : {tournament_data["number of rounds"]}')
        print(f'Tournament current round : {tournament_data["tournament current round"]}')
        print(f'Tournament round list: " {tournament_data["tournament round list"]}')
        print(f'Tournament Players :  {tournament_data["tournament player list"]}')
        print(f'Tournament description : {tournament_data["description"]}')

    # def display_tournament_repport(self, player_list, tournament_data,):

    def get_tournament_data(self, player_list, current_round, tournament_round_list):
        """
        Get all the information for the tournament
        """
        tournament_name = input("Right the name of the tournament: ")
        tournament_place = input("Right the place of the tournament: ")

        tournament_start_date = input("Right the date of the tournament dd/mm/yyyy: ")
        tournament_end_date = input("Right the end date of the tournament dd/mm/yyyy: ")
        tournament_number_of_round = int(input("Right the number of round: "))
        tournament_description = input("Right the description of the tournament")

        tournament_data = {
            "name": tournament_name,
            "place": tournament_place,
            "date": tournament_start_date + tournament_end_date,
            "number of round": tournament_number_of_round,
            "tournament current round": current_round,
            "Tournament player list": player_list,
            "description": tournament_description,
            "tournament round list": tournament_round_list
            }

        return tournament_data

    def tournament_choose_player(self):
        """fonction to choose a player for a tournament"""

        print("1 - Right chess ID of the player to choose member of the tournament")
        print("2 - choose player by a list")
        print("Q - Exit players selection")
        choice = input("Do your choice: ")

        return choice

    def tournament_score_menu(self):
        """score for a tournament"""
        print("1 - Right ID of the player to score")
        print("2 - Choose player from the tournament list")
        print("R - Return to the selection menu")
        print("Q - Exit players selection")
        choice = input("Do your choice: ")

        return choice
