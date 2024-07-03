# from chess.controllers.main_controller import

from rich.table import Table
from rich.console import Console
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

    def display_tournament_table(self, tournament_data):
        """Display all the information of a tournament"""
        print("\n -------Tournament data-------")
        table = Table(title=f"Tournament{tournament_data['name']}")
        table.add_column("name", justify="right", style="cyan", no_wrap=True)
        table.add_column("place", justify="center", style="purple")
        table.add_column("date", justify="right", style="magenta")
        table.add_column("player list", justify="right", style="green")
        table.add_column("number of rounds", justify="right", style="green")
        table.add_column("description", justify="right", style="green")

        table.add_row(
            tournament_data['name', 'N/A'],
            tournament_data['place', 'N/A'],
            tournament_data['start date', 'N/A'],
            tournament_data['end date', 'N/A'],
            tournament_data['player list', 'N/A'],
            tournament_data['number of round'],
            tournament_data['description']
            )

        console = Console()
        console.print(table)

    def get_tournament_data(self):
        """
        Get  information for the tournament
        """
        tournament_name = input("Right the name of the tournament: ")
        tournament_place = input("Right the place of the tournament: ")
        tournament_description = input("Right the description of the tournament: ")

        while True:
            tournament_start_date = input("Right the date of the tournament dd/mm/yyyy: ")
            try:
                start_date = datetime.strptime(tournament_start_date, "%d/%m/%Y")
                break
            except ValueError:
                print("Incorrect data format, should be dd/mm/yyyy")

        while True:
            tournament_end_date = input("Right the end date of the tournament dd/mm/yyyy: ")
            try:
                end_date = datetime.strptime(tournament_end_date, "%d/%m/%Y")
                if end_date < start_date:
                    print("End date cannot be before start date")
                    continue
                break

            except ValueError:
                print("Incorrect data format, should be dd/mm/yyyy")

        tournament_data = {
            "name": tournament_name,
            "place": tournament_place,
            "start date": start_date.strftime("%d/%m/%Y"),
            "end date": end_date.strftime("%d/%m/%Y"),
            "description": tournament_description
            }

        return tournament_data

    def round_tournament(self):
        """Create a round for the tournament"""
        number_of_round = input("Rigth your desire number of round (default:4): ")
        if number_of_round:
            return number_of_round
        else:
            return None

    def tournament_choose_player(self):
        """fonction to choose a player for a tournament"""

        print("\n ---- choose player by a list----")

        choice = input("Do your choice (right number separate by / or ,): ")

        return choice

    def tournament_score_menu(self):
        """score for a tournament"""
        print("1 - Right ID of the player to score")
        print("2 - Choose player from the tournament list")
        print("R - Return to the selection menu")
        print("Q - Exit players selection")
        choice = input("Do your choice: ")

        return choice
