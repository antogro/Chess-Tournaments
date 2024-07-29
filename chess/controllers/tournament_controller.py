
from ..views.round_view import RoundView
from chess.views.tournament_view import TournamentsView
from chess.models.tournament_model import TournamentModel, TournamentPlayer, TournamentManager, RoundModels, Match
import random as rd
from  datetime import datetime
from chess.models.player_model import Player

from chess.views.base_views import Display
# from chess.models.player_model import Player


class TournamentControl:
    """fonction to control the tournament"""

    def __init__(self):
        self.tournament_view = TournamentsView()

        self.control_tournament = ControlTournament()

    def manage_tournament(self):
        """manage the tournament"""
        while True:
            choice = self.tournament_view.display_tournament_menu()
            if choice == "1":
                """creat tournament"""
                self.control_tournament.creat_tournament()
                

            elif choice == "2":
                """Continue the last tournament"""
                self.control_tournament.continue_last_tournament()

            elif choice == "3":
                """select and start round"""
                self.control_tournament.select_and_continue_tournament()
                break
            elif choice == "4":
                """show list of tournament"""
                self.control_tournament.display_all_tournament()

            elif choice == "5":
                """back to main menu"""

                break
            elif choice == "Q" or choice == "q":
                """exit"""
                break


class ControlTournament:
    """manage the tournament"""

    def __init__(self):
        self.tournament_view = TournamentsView()
        self.tournament_manager = TournamentManager()

        self.round_view = RoundView()
        self.display = Display()
      
        self.tournament_player = TournamentPlayer(self)
        self.players = Player(self, self, self, self, self, self)
        pass

    def creat_tournament(self):
        """creat tournament"""
        tournament_data = self.tournament_view.get_tournament_data()
        tournament = TournamentModel(**tournament_data)
        tournament = self.tournament_manager.id_tournament(tournament)

        self.display.display_table("Player list", [player for player in self.players.all()])

        players_id = self.tournament_view.tournament_choose_player()
        tournament = self.tournament_player.add_player(players_id, tournament)



        self.tournament_manager.save(tournament)

        self.display.display_table("Tournament: ", [tournament.to_dict])
        self.display.display_table("Player list: ", [player.player.to_dict for player in tournament.players])
        
        self.manage_round(tournament)

    def display_all_tournament(self):
        """display tournament"""
        tournaments = self.tournament_manager.load_all_tournament()
        self.display.display_table("Tournament", [tournament for tournament in tournaments])

    def continue_last_tournament(self):
        tournament_id = self.tournament_manager.get_last_tournament_id()
        tournament = self.tournament_manager.load_tournament(tournament_id)
        player_data = self.tournament_player.link_player(tournament.players)
        self.display.display_table("Tournament: ", [tournament.to_dict])
        self.display.display_table("Player list: ", [linked.to_dict for linked in player_data])
     
    def select_and_continue_tournament(self):
        tournaments = self.tournament_manager.load_all_tournament()
        self.display.display_table("Tournament", [tournament for tournament in tournaments])
        id = self.display.display_input("Right the number of the id: ")
        tournament = self.tournament_manager.load_tournament(int(id))
        player_data = self.tournament_player.link_player(tournament.players)
        self.display.display_table("Tournament: ", [tournament.to_dict])
        self.display.display_table("Player list: ", [linked.to_dict for linked in player_data])
       

    def manage_round(self, tournament):
        """manage round"""

        round_continue = True

        while round_continue:
            choice = self.round_view.manage_round_view()
            if choice != "1":
                tournament.paused
                self.tournament_manager.update_tournament(tournament)
                break

            round = None

            players = tournament.players

            if round is None:
                if tournament.current_round == 1:
                    rd.shuffle(players)
                else:
                    players.sort(reversed=True, key=lambda player: (player.score, player.doc_id))
            
                round = self.creat_round(tournament)
          
                
                self.get_matches(round)
            tournament.rounds.append(round)

            round_choice = self.manage_score(round)
            if round_choice == "2":
                TournamentModel.paused
                TournamentManager.update_tournament
                break
            
            tournament.current_round += 1

            if tournament.current_round >= int(tournament.number_of_round):
                print("Tournament has reached the maximum number of rounds")
                round_continue = False
                TournamentModel.finished
                tournament.end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                tournament.status
                self.display.display_message(f"The tournament: {tournament.name} is finished")
                self.display.display_table
            else:
                self.display.display_message(f"Round {tournament.current_round - 1} is finished")
                self.display.display_message(f"Initialization of the {tournament.current_round} round")

    def creat_round(self, tournament: TournamentModel) -> RoundModels:
        """creat round"""
        matches = []
        name = f"Round {tournament.current_round}"
        date = datetime.now()
        start_date = date.strftime("%d-%m-%Y %H:%M:%S")
        players = tournament.players.copy()
        while len(players) > 1:
            player_1 = players.pop(0)
            player_2 = players.pop(0)
            match = Match(player_1, player_2)
            matches.append(match)

        tournament.rounds.append(RoundModels(matches=matches, start_date=start_date, name=name))
     
        return tournament

    def get_matches(self, round: RoundModels):
        print('round: ', round.matches[1].player1_score.player.full_name)

        title = f'Opponent match list: {round.name}'
        matches = []
        for index, match in enumerate(round.matches):

            matches.append(
                {
                "Matche": str(index +1),
                "Player 1": match.player1_score.player.full_name,
                "Player 2": match.player2_score.player.full_name
            }
            )
        headers = ["Matche", "Player 1", "Player 2"]

        print('matches: ', matches)
        self.display.display_table(title, [match for match in matches], headers)

    def manage_score(self, round: RoundModels):
 
        choice = self.round_view.get_round_choice()

        if choice != "1":
            return "2"
       
        for pairing in round.matches:
            result = self.round_view.get_match_result(pairing, round.name)
       

            if result == "1":
                pairing.player1_score.score = 1.0
                self.round_view.display_match_result(pairing.player1_score.player.full_name)
            elif result == "2":
                pairing.player2_score.score += 1
                self.round_view.display_match_result(pairing.player2_score.player.full_name)
            elif result == "0":
                self.round_view.display_match_result(None, is_draw=True)
                pairing.player1_score.score = 0.5
                pairing.player2_score.score = 0.5
            
            round.end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            round.status = "Finished"
            
        return round
