import json
from typing import Dict, Any
import pathlib


class SavePlayer:
    """
    Permet de sauvegarder le informations des joueurs
    """
    def __init__(self, player_data: Dict[str, Any]):
        self.player_data = player_data

    def save_new_player(self):
        """
        Sauvegarde un nouveau joueur
        """
        player_file_path = pathlib.Path('data/players.json')

        if not player_file_path.exists():
            player_file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open("players.json", "r") as file:
                player_data_json = json.load(file)
        except FileNotFoundError:
            player_data_json = {}

        player_id = self.player_data["chess_id"]
        if player_id not in player_data_json:
            player_data_json[player_id] = self.player_data

        with open("players.json", "w") as file:
            json.dump(player_data_json, file, indent=4)


def choose_player():
    player_in_tournament = []
    with open("players.json", "r") as file:
        players = json.load(file)
        while True:
            print("1 - Right ID of the player to choose member of the tournament")
            print("2 - Exit players selection")
            choice = input("Do your choice")
            if choice == "1":
                player_id = input("Right the player ID: ")
                players.append(player_id)
            for player in players:
                player_in_tournament.append(player["first_name", "second_name"])
                print(player_in_tournament)
