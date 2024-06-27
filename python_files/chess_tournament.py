import re
import json
import pathlib
from typing import Dict, Any
from datetime import datetime


class Player:
    def __init__(self, first_name: str, second_name: str, date_birth: str, player_id: str):
        self.first_name = first_name
        self.second_name = second_name
        self.date_birth = date_birth
        self.player_id = player_id


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


def data_player():
    first_name = input("Rentrer votre nom: ")
    second_name = input("Rentrer votre prénom: ")
    date_birth = input("Rentrer votre date de naissance: ")
    chess_ID = input("Rentrer votre ID de jeu: ")

    player_data = {
        "first_name": first_name,
        "second_name": second_name,
        "Date_birth": date_birth,
        "chess_id": chess_ID
        #"player point": 
    }
    return player_data


def tournament():
    """
    Permet de sauvegarder les informations d'un tournoi
    """
    tournament_name = input("Right the name of the tournament: ")
    tournament_place = input("Right the place of the tournament: ")

    tournament_start = input("Right the date of the tournament dd/mm/yyyy: ")
    tournament_end = input("Right the end date of the tournament dd/mm/yyyy: ")
    tournament_date = verify_date(tournament_start, tournament_end)
    if tournament_date:
        tournament_start_date, tournament_end_date = tournament_date

    try:
        tournament_number_of_round = int(input("Right the number of round: "))
    except ValueError:
        tournament_number_of_round = 4

    tournament_data = {
        "tournament name": tournament_name,
        "tournament date": tournament_start_date,
        "tournament end_date": tournament_end_date,
        "tournament place": tournament_place,
        "number_of_round": tournament_number_of_round
        }

    print(tournament_data)


def verify_date(tournament_start, tournament_end):

    tournament_start = tournament_start.replace("/", "")
    tournament_end = tournament_end.replace("/", "")

    if re.match(r'^\d{8}$', tournament_start) or not re.match(r'^\d{8}$', tournament_end):
        return None

    try:
        tournament_start_date = datetime.strptime(tournament_start, "%d%m%Y")
        tournament_end_date = datetime.strptime(tournament_end, "%d%m%Y")

        if tournament_end_date < tournament_start_date:
            return None

        return (tournament_start_date.strftime("%d/%m/%Y"),
                tournament_end_date.strftime("%d/%m/%Y"))

    except ValueError:
        return None


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
