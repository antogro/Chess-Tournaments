from chess.controllers.main_controller import 
from tinydb import TinyDB as db
import json



class TournamentsView:
    """Show the information of a tournament"""

    def display_tournament(self, tournament):
        print("Tournament name: " + tournament.name)
        print("Tournament date: " + tournament.date)
        print("Tournament place: " + tournament.place)
        print("Tournament number of rounds: " + str(tournament.number_of_rounds))
        print("Tournament round list: " + tournament.round_list)
        print("Tournament Players : " + tournament.player_list)
        print("Tournament description: " + tournament.description)


    def get_tournament_data(self, player_list):
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
            "tournament name": tournament_name,
            "tournament date": tournament_start_date,
            "tournament end date": tournament_end_date,
            "tournament place": tournament_place,
            "number of round": tournament_number_of_round,
            "Tournament player": player_list,
            "description": tournament_description
            }

        return tournament_data
    

    def display_player_list(self):
        """Show the list of the player"""
        table = db.table("player_list")
        table.insert({'value': True})
        table.all
        

    def choose_player(self):
        
            while True:
                print("1 - Right ID of the player to choose member of the tournament")
                print("2 - Exit players selection")
                choice = input("Do your choice: ")
                if choice == "1":
                    player_id = input("Right the player ID: ")
                    players.append(player_id)
                for player in players:
                    player_in_tournament.append(player["first_name", "second_name"])
                    print(player_in_tournament)