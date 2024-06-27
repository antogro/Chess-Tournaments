from chess.controllers.application_controller import 



class TournamentsView:
    """Show the information of a tournament"""

    def display_tournament(self, tournament):
        print("Tournament name: " + tournament.name)
        print("Tournament date: " + tournament.date)
        print("Tournament place: " + tournament.place)
        print("Tournament number of rounds: " + str(tournament.number_of_rounds))
        print("Tournament round list: " + tournament.round_list)
        print("Tournament Players : " + tournament.list_player)
        print("Tournament description: " + tournament.description)


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