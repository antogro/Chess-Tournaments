from datetime import datetime
from chess.models.tournament_model import TournamentModel, TournamentPlayer,TournamentManager, TournamentPlayerManager
from chess.views.round_view import RoundView
from chess.models.table_manager import TableManager
from chess.models.pairing_manager import PairingManager
from chess.models.data_manager import ManageData
from chess.models.round_model import RoundModels, RoundManager, Match
from chess.views.player_view import PlayerView


class RoundControl:
    def __init__(self):
        self.round_tournament = RoundTournament()
        self.round_view = RoundView()

    def round(self, tournament_data, tournement_id, player_data):

        while True:
            choice = self.round_view.manage_round_view()
            if choice == "1":
                """start round"""
                self.round_tournament.manage_round(tournament_data, tournement_id, player_data)
                continue
            elif choice == "2":
                """Paused round"""
                self.round_tournament.paused_round(tournament_data, pairings=None)

                break

            elif choice == "3":
                break


class RoundTournament:
    def __init__(self):
        self.table_manager = TableManager()

        self.data_manager = ManageData()
        self.round_manager = RoundManager(self.table_manager, self.data_manager)
        self.round_model = RoundModels(self, self, self, self)
        self.round_view = RoundView()
        self.pairing_manager = PairingManager(self.table_manager)
        self.tournament_player_manager = TournamentPlayerManager()
        self.tournament_manager = TournamentManager()
        self.player_view = PlayerView()
        self.tournament_model_player = TournamentPlayer(self, self, self, self)

    def manage_round(self, tournaments, tournament_id, player_data):
        """manage round"""
        TournamentModel.resume
        self.table_manager.display_table("Tournament: ", [tournaments.to_dict])
        
        tournament, pairings = self.get_or_creat_pairing(tournaments, player_data)
        
        TournamentManager.update        

        extract_data = self.round_manager.extract_and_display_round(pairings)


        if self.round_view.get_round_choice() == "1":
            self.play_round(extract_data, tournament)
        else:
            self.paused_round(tournament)
            return

    def get_or_creat_pairing(self, tournament, players):
        """get or creat pairing"""
        current_round = tournament.current_round

        round_key = f"round {current_round}"
        if round_key in tournament.matches:
            round_model_data = tournament.matches[round_key]
            return [Match.from_dict(match_data) for match_data in round_model_data["matches"]]

        if current_round == 1:
            pairings = self.pairing_manager.creat_pairing_first_round(players)



            if round_key not in tournament.matches:
                tournament.matches[round_key] = RoundModels(name=f"Round {current_round}", _start_date=datetime.now())
        
            tournament.matches[round_key] = pairings
            

            return tournament, pairings
        else:
            return self.round_model.creat_pairing_next_round(tournament_data)

    def play_round(self, pairings, tournament):        
        """play round"""
        

        update_pairing = self.manage_score(pairings, tournament)
        tournament.next_round
        tournaments = self.tournament_manager.update(
            tournament, update_pairing
        )
        self.round_manager.extract_and_display_round(tournament, player_data)

    # def manage_rond(self, tournament_data, tournament_id):
    #     """manage round"""
    #     tournament_data = self.round_model.mixed_player(tournament_data)
    #     player_data = self.tournament_model_player.extract_player_list(tournament_data)

    #     if tournament_data["current_round"] == 1:
    #     else:
    #         pairings = self.round_model.creat_pairing_next_round(tournament_data)

    #     choice = self.round_view.get_round_choice()

    #     if choice == "1":
    #         update_pairings = self.manage_score(pairings, tournament_data)

    #     else:
    #         self.round_view.display_round_paused()
    #         tournament_data = self.round_model.update_tournament_data(
    #             tournament_data, pairings
    #         )
    #         self.tournament_model = TournamentModel(**tournament_data)
    #         self.tournament_model.paused_tournament(tournament_id)

    #     if self.tournament_model.current_round >= int(
    #         tournament_data["number_of_round"]
    #     ):
    #         print("match finish")

    def manage_score(self, pairings, tournament_data):

        for pairing in pairings:
            player1 = TournamentPlayer(**pairing['player1'])
            player2 = TournamentPlayer(**pairing['player2'])

            result = self.round_view.get_match_result(player1, player2, tournament_data)
            player1.score = float(player1.score)
            player2.score = float(player2.score)

            if result == "1":
                player1.score += 1
                self.round_view.display_match_result(player1.first_name)
            elif result == "2":
                player2.score += 1
                self.round_view.display_match_result(player2.first_name)
            elif result == "0":
                self.round_view.display_match_result(None, is_draw=True)
                player1.score += 0.5
                player2.score += 0.5
            player1.score = str(player1.score)
            player2.score = str(player2.score)

            pairing["end_date"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        return pairings

    def paused_round(self, tournament, pairings):
        tournaments = TournamentModel(**tournament)
        tournaments.paused

        tournament = self.tournament_manager.update(
            tournament, pairings
        )
        
        self.round_view.display_round_paused()
