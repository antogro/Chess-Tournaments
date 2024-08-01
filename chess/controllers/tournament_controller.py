import random as rd
from typing import List
from  datetime import datetime
from ..views.round_view import RoundView
from ..views.base_views import Display
from ..models.player_model import Player
from ..views.tournament_view import TournamentsView
from ..models.tournament_model import TournamentModel, TournamentPlayer, TournamentManager, RoundModels, Match


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
                try:
                    self.control_tournament.select_and_continue_tournament()
                except Exception as e:
                    print(e)
                break
            elif choice == "4":
                """select and repport a tournament"""
                self.control_tournament.select_and_report_tournament()
                break

            elif choice == "5":
                """show list of tournament"""
                self.control_tournament.display_all_tournament()
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

        pass

    def creat_tournament(self):
        """Create a new tournament, add players, save it, and start managing rounds."""

        tournament_data = self.tournament_view.get_tournament_data()
        tournament = TournamentModel(**tournament_data)
        tournament = self.tournament_manager.id_tournament(tournament)

        self.display.display_table("Player list", [player for player in Player.all()])
        players_id = self.tournament_view.tournament_choose_player()
        tournament = self.tournament_player.add_player(players_id, tournament)
        self.tournament_manager.save(tournament)

        self.display.display_table("Tournament: ", [tournament.to_dict])
        self.display.display_table("Player list: ", [player.player.to_dict for player in tournament.players])
        self.manage_round(tournament)

    def display_all_tournament(self):
        """Display all tournament from the data base"""
        tournaments = self.tournament_manager.load_all_tournament()
        self.display.display_table("Tournament", [tournament for tournament in tournaments])

    def continue_last_tournament(self):
        """Continue the last tournament from the database"""
        last_tournament_id = self.tournament_manager.get_last_tournament_id()
        if last_tournament_id:
            tournament = self.tournament_manager.load_tournament(last_tournament_id)
            self.display.display_table("Tournament: ", [tournament.to_dict])
            self.display_player([player for player in tournament.players])
            self.manage_round(tournament)
        else:
            self.display.display_message("No tournament found!")
     
    def select_and_continue_tournament(self):
        """Select a tournament and to continue it"""
        tournaments = self.tournament_manager.load_all_tournament()
        self.display.display_table("Tournament", [tournament for tournament in tournaments])
        
        while True:
            try:
                id = self.display.display_input("Right the number of the id: ")
                tournament = self.tournament_manager.load_tournament(int(id))
            
                if tournament:
                    self.display.display_table("Tournament: ", [tournament.to_dict])
                    self.display_player([player for player in tournament.players])
                    self.manage_round(tournament)
                    break
            
                self.display.display_message("Tournament not found!")
            except ValueError:
                self.display.display_error_input()

    def select_and_report_tournament(self, repport=None):
        """Select a tournament and report it"""
        tournaments = self.tournament_manager.load_all_tournament()
        repport = True
        while repport:    
            self.display.display_table("Tournament", [tournament for tournament in tournaments], exclude_headers=['rounds'])
            id = self.display.display_input("Right the number of the id: ")
            try:
                tournament = self.tournament_manager.load_tournament(int(id))
                break
            except ValueError as e:
                self.display.display_message(f"{e}")
                continue
        self.repport(tournament)
    
    def repport(self, tournament: TournamentModel):
        """Fonction to report a tournament"""
        while True:
            choice = self.tournament_view.select_repport_tournament_by_classment()
            if choice == "1":
                player = sorted(tournament.players, key=lambda x: x.player.last_name)
                break
            elif choice == "2":
                player = sorted(tournament.players, key=lambda x: x.score, reverse=True)
                break
            else:
                self.display.display_error_input()
        self.display.display_table("Tournament: ", [tournament.to_dict])
        for rounds in tournament.rounds:
                    self.get_repport(rounds)
        self.tournament_player.update_player_scores(tournament)
        self.display_player(player)

    def manage_round(self, tournament: TournamentModel):
        """manage round, organise opponent"""

        round_continue = True
        while round_continue:
            if tournament.current_round > int(tournament.number_of_round):
                self.display.display_message("--- The tournament is already end! ---\n")
                break
            else:
                choice = self.round_view.manage_round_view()
                if choice != "1":
                    tournament.paused()
                    self.tournament_manager.update_tournament(tournament)
                    break
                
                tournament.resume()
                round = None
                players = tournament.players

                if round is None:
                    if tournament.current_round == 1:
                        rd.shuffle(players)
                    else:
                        players.sort(reverse=True, key=lambda player: (player.score, player.player.doc_id))
                
                    rounds = self.creat_round(tournament)
                    self.get_matches(rounds)
            
                round_choice = self.manage_score(rounds)

                if round_choice == "2":
                    tournament.paused()
                    self.tournament_manager.update_tournament(tournament)
                    break
                else:
                    tournament.rounds.append(round_choice)
                    self.tournament_manager.update_tournament(tournament)
                tournament.current_round += 1
                
                if tournament.current_round > int(tournament.number_of_round):
                    self.display.display_message("Tournament has reached the maximum number of rounds")
                    round_continue = False
                    tournament.finished()
                    tournament.end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    self.tournament_manager.update_tournament(tournament)
                    self.display.display_message(f"The tournament: {tournament.name} is finished")
                    self.repport(tournament)
                
                else:
                    self.tournament_manager.update_tournament(tournament)
                    self.display.display_message(f"Round {tournament.current_round - 1} is finished")
                    self.display.display_message(f"Initialization of the {tournament.current_round} round")

    def creat_round(self, tournament: TournamentModel) -> RoundModels:
        """Creat and built opponnent for the current round"""
        matches = []
        name = f"Round {tournament.current_round}"
        start_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        players = tournament.players.copy()
        while len(players) > 1:
            player_1 = players.pop(0)
            player_2 = players.pop(0)
            match = Match(player_1, player_2)
            match.format_data(match)
            matches.append(match)

        rounds = RoundModels(matches=matches, start_date=start_date, name=name)
        return rounds

    def get_matches(self, rounds: RoundModels):
        """Display opponent for the current round"""
        title = f'Opponent match list: {rounds.name}'
        matches = []
        for index, match in enumerate(rounds.matches):

            matches.append(
                {
                "Matche": str(index +1),
                "Player 1": match.player1_score.player.full_name,
                "Player 2": match.player2_score.player.full_name
            }
            )
        headers = ["Matche", "Player 1", "Player 2"]
        self.display.display_table(title, [match for match in matches], headers)

    def manage_score(self, round: RoundModels):
        """Add score to players"""
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
            pairing.end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return round
   
    def get_repport(self, rounds: RoundModels):
        """Display repport of player"""

        title = f'Opponent match list: {rounds.name}'
        matches = []
        for index, match in enumerate(rounds.matches):

            matches.append(
                {
                "Matche": str(index +1),
                "Player 1": match.player1_score.player.full_name,
                "Player 1 score": match.player1_score.score,
                "Player 2": match.player2_score.player.full_name,
                "Player 2 score": match.player2_score.score,
            }
            )
        headers = ["Matche", "Player 1", "Player 1 score", "Player 2", "Player 2 score"]
        self.display.display_table(title, [match for match in matches], headers)

    def display_player(self, players: List[TournamentPlayer]):
        title = 'Players list:'
        players_list = []
        for player in players:
            players_list.append({
                "ID": player.player.doc_id,
                "First Name": player.player.first_name,
                "Last Name": player.player.last_name,
                "Score": player.score
            })
        headers = ["ID", "First Name", "Last Name", "Score"]
        self.display.display_table(title, players_list, headers)