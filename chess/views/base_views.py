from rich.table import Table
from rich.console import Console
import os


class Display:

    def __init__(self) -> None:
        self.console = Console()

    def clear_screen(self):
        """Reset console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_table(
        self, title: str,
        items: list[dict],
        headers: list = [],
        exclude_headers=None
    ):
        """display table data with ritch table"""
        print("\n")

        table = Table(
            title=title,
            padding=(0, 1),
            header_style="blue",
            title_style="purple",
            min_width=60,
        )

        if not headers:
            try:
                headers = list(items[0].keys())
            except IndexError:
                headers = []

        if exclude_headers:
            headers = [header for header in headers
                       if header not in exclude_headers]

        for title in headers:
            table.add_column(str(title), justify="center", style="cyan")

        for item in items:
            values = [str(item.get(header, "")) for header in headers]
            table.add_row(*values)

        print("")
        self.console.print(table)

    def display_input(self, message: str):
        """display input message"""
        print(f"\n{message}")
        return input("Do your choice: ")

    def display_error_input(self):
        """display error message input"""
        print("\n")
        print("Error: Invalid input")
        print("\n")

    def display_error_message(self, message: str):
        print(f"Error : {message}")

    def display_message(self, message: str):
        print(f"\n{message}")

    def display_player(self, players: list, exclude_headers=None):
        """display player data for repport with ritch table"""
        title = "Players list:"

        players_list = [
            {
                "ID": player.doc_id,
                "First Name": player.first_name,
                "Last Name": player.last_name,
                "Score": player.score,
            }
            for player in players
        ]

        headers = ["ID", "First Name", "Last Name", "Score"]
        self.display_table(
            title,
            players_list,
            headers,
            exclude_headers=exclude_headers,
        )

    def get_repport(self, rounds):
        """Display repport of player"""
        title = f"Opponent match list: {rounds.name}"
        matches = []
        for index, match in enumerate(rounds.matches):

            matches.append(
                {
                    "Match": str(index + 1),
                    "Player 1": match.player1_score.player.full_name,
                    "Player 1 score": match.player1_score.score,
                    "Player 2": match.player2_score.player.full_name,
                    "Player 2 score": match.player2_score.score,
                }
            )
        headers = ["Match",
                   "Player 1",
                   "Player 1 score",
                   "Player 2",
                   "Player 2 score"]

        self.display_table(title,
                           [match for match in matches],
                           headers)

    def get_matches(self, rounds):
        """Display opponent for the current round"""
        title = f"Opponent match list: {rounds.name}"
        matches = []
        for index, match in enumerate(rounds.matches):

            matches.append(
                {
                    "Match": str(index + 1),
                    "Player 1": match.player1_score.player.full_name,
                    "Player 2": match.player2_score.player.full_name,
                }
            )
        headers = ["Match", "Player 1", "Player 2"]
        self.display_table(
            title,
            [match for match in matches],
            headers,
            exclude_headers=["score"]
        )
