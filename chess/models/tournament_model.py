

class TournamentModel:
    def __init__(self) -> None:
        pass

    def creat_tournament(self):
        if tournament_date:
            tournament_start_date, tournament_end_date = tournament_date

        try:
            tournament_number_of_round = int(input("Right the number of round: "))
        except ValueError:
            tournament_number_of_round = 4


    def choose_player(self):
        player_in_tournament = []
        with open("players.json", "r") as file:
            players = json.load(file)