from rich.table import Table
from rich.console import Console
from chess.models.tournament_model import TournamentPlayer


class TableManager:
    def __init__(
        self,
    ):
        self.tournament_model = TournamentPlayer()
        pass

    def display_player_table(self, player_list):
        table = Table(title="Player list")

        table.add_column("doc_id", style="black")
        table.add_column("first_name", style="cyan", no_wrap=True)
        table.add_column("last_name", style="magenta")
        table.add_column("birth_date", style="green")
        table.add_column("chess_id", style="yellow")
        table.add_column("score", style="red")

        for player in player_list:
            table.add_row(
                str(player.get("doc_id", "N/A")),
                player.get("first_name", "N/A"),
                player.get("last_name", "N/A"),
                player.get("birth_date", "N/A"),
                player.get("chess_id", "N/A"),
                str(player.get("score", "N/A")),
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

        if not tournament_data.get("name"):
            tournament_name = "Chess Tournament"
        else:
            tournament_name = tournament_data.get("name")

        tournament_table = Table(title=f"Tournoi d'échec : {tournament_name}!")
        tournament_table.add_column("Attribut", style="cyan")
        tournament_table.add_column("Valeur", style="magenta")

        # Ajouter les lignes au tableau en vérifiant l'existence des clés
        for key, display_name in [
            ("doc_id", "ID du Tournoi"),
            ("name", "Nom"),
            ("place", "Lieu"),
            ("start_date", "Date de début"),
            ("end_date", "Date de fin"),
            ("number_of_round", "Nombre de tours"),
            ("description", "Description"),
            ("current_round", "Tour actuel"),
            ("match", "Match"),
            ("status", "Status"),
        ]:
            value = tournament_data.get(key, "N/A")
            tournament_table.add_row(display_name, str(value))

        console.print(tournament_table)

    def display_player_list_table(self, tournament_data):
        console = Console()
        player_table = None
        if "player_list" in tournament_data:
            player_table = Table(title="Liste des joueurs du tournoi")
            player_table.add_column("Prénom", style="green")
            player_table.add_column("Nom", style="green")
            player_table.add_column("ID Echecs", style="yellow")
            player_table.add_column("Classement", style="red")

        player_list = tournament_data["player_list"]

        for player in player_list:
            player_table.add_row(
                str(player["first_name"]),
                str(player["last_name"]),
                str(player["chess_id"]),
                str(player.get("score", "N/A")),
            )

        console.print(player_table)

    def display_round_table(self, linked_match_data):
        """Display the round table using data from link_player_names"""
        console = Console()

        # Assurez-vous que tous les champs sont des chaînes de caractères
        for match in linked_match_data:
            match["round"] = str(match.get("round", ""))
            match["match"] = str(match.get("match", ""))
            match["player1"]["name"] = str(match["player1"].get("name", ""))
            match["player1"]["score"] = str(match["player1"].get("score", ""))
            match["player2"]["name"] = str(match["player2"].get("name", ""))
            match["player2"]["score"] = str(match["player2"].get("score", ""))
            match["start_date"] = str(match.get("start_date", ""))
            match["end_date"] = str(match.get("end_date", ""))

        rounds = set(match["round"] for match in linked_match_data if "round" in match)

        for round_key in sorted(rounds):
            round_matches = [
                match for match in linked_match_data if match["round"] == round_key
            ]
            round_table = Table(title=f"Résultats des matchs - {round_key}")
            round_table.add_column("Round", style="cyan")
            round_table.add_column("Match", style="cyan")
            round_table.add_column("Joueur 1", style="green")
            round_table.add_column("Score J1", style="green")
            round_table.add_column("Joueur 2", style="purple")
            round_table.add_column("Score J2", style="purple")
            round_table.add_column("Date début", style="yellow")
            round_table.add_column("Date fin", style="yellow")

            for match in round_matches:
                # Impression pour le débogage
                player1_name = (
                    match["player1"]["name"] if match["player1"]["name"] else "N/A"
                )
                player2_name = (
                    match["player2"]["name"] if match["player2"]["name"] else "N/A"
                )

                round_table.add_row(
                    match["round"],
                    match["match"],
                    player1_name,
                    match["player1"]["score"],
                    player2_name,
                    match["player2"]["score"],
                    match["start_date"],
                    match["end_date"] if match["end_date"] else "En cours",
                )

            console.print(round_table)
            console.print("\n")
