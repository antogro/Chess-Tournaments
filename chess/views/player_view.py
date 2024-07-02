from rich.table import Table
from rich.console import Console


class PlayerView:
    def __init__(self, ) -> None:
        pass

    def display_player_menu(self):
        print("1. Create a new player")
        print("2. Players list")
        print("3. Show user by chess ID")
        print("4. Exit")
        menu_player = input("Right your choose number: ")

        return menu_player

    def get_chess_id(self):
        chess_id = input("Right your chess id: ")
        return chess_id

    def add_player(self, chess_id):
        print("\n--- Add a new player ---")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        birth_date = input("birth date : ")
        chess_ID = chess_id

        player_data = {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "chess_id": chess_ID
            # "player point":
        }
        return player_data

    def display_new_player(self, player_add):
        print("New player created: " + player_add["first_name"])

    def display_error_message(self, message):
        print("Error :" + message)

    def display_player_table(self, player_list):
        table = Table(title="Player list")

        table.add_column("Doc_ID", style="black")
        table.add_column("first_name", style="cyan", no_wrap=True)
        table.add_column("last_name", style="magenta")
        table.add_column("birth_date", style="green")
        table.add_column("chess_id", style="yellow")

        for player in player_list:
            table.add_row(
                str(player.get("doc_id")),
                player.get('first_name', 'N/A'),
                player.get('last_name', 'N/A'),
                player.get('birth_date', 'N/A'),
                player.get('chess_id', 'N/A')
                )

        console = Console()
        console.print(table)
        print(table)
