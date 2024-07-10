from rich.table import Table
from rich.console import Console


class TableManager:
    def __init__(
        self,
    ):
        pass

    def display_player_table(self, player_list):
        table = Table(title="Player list")

        table.add_column("doc_ID", style="black")
        table.add_column("first_name", style="cyan", no_wrap=True)
        table.add_column("last_name", style="magenta")
        table.add_column("birth_date", style="green")
        table.add_column("chess_id", style="yellow")
        table.add_column("rank", style="red")

        for player in player_list:
            table.add_row(
                str(player.get("doc_ID", "N/A")),
                player.get("first_name", "N/A"),
                player.get("last_name", "N/A"),
                player.get("birth_date", "N/A"),
                player.get("chess_id", "N/A"),
                str(player.get("rank", "N/A")),
            )

        console = Console()
        console.print(table)

    def display_tournament_table(self, tournament_data):
        """Display all the information of a tournament"""
        print("\n -------Tournament data-------")
        console = Console()

        if isinstance(tournament_data, list):

            if len(tournament_data) > 0:
                tournament_data = tournament_data[0]

        assert isinstance(tournament_data, dict)

        tournament_table = Table(
            title=f"Tournoi d'échec : {tournament_data.get('name')}!"
        )
        tournament_table.add_column("Attribut", style="cyan")
        tournament_table.add_column("Valeur", style="magenta")

        # Ajouter les lignes au tableau en vérifiant l'existence des clés
        for key, display_name in [
            ("name", "Nom"),
            ("place", "Lieu"),
            ("start date", "Date de début"),
            ("end date", "Date de fin"),
            ("number of round", "Nombre de tours"),
            ("description", "Description"),
            ("current round", "Tour actuel"),
            ("match", "Match"),
            ("status", "Status"),
        ]:
            value = tournament_data.get(key, "N/A")
            tournament_table.add_row(display_name, str(value))

        console.print(tournament_table)

        if "player_list" in tournament_data and tournament_data.get("name"):
            player_table = Table(
                title=f"Liste des joueurs du tournoi: {tournament_data.get('name')}"
            )
            player_table.add_column("Prénom", style="green")
            player_table.add_column("Nom", style="green")
            player_table.add_column("ID Echecs", style="yellow")
            player_table.add_column("Classement", style="red")

        for player in tournament_data["player_list"]:
            player_table.add_row(
                str(player["first_name"]),
                str(player["last_name"]),
                str(player["chess_id"]),
                str(player.get("rank", "N/A")),
            )

        console.print(player_table)
