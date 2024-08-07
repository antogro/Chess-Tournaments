import random as rd
from datetime import datetime
from ..views.round_view import RoundView
from ..views.base_views import Display
from ..models.player_model import Player
from ..views.tournament_view import TournamentsView
from ..models.tournament_model import (
    TournamentModel,
    TournamentPlayer,
    TournamentManager,
    RoundModels,
    Match,
)


class TournamentControl:
    """fonction to control the tournament"""

    def __init__(self):
        self.tournament_view = TournamentsView()
        self.display_repport = DisplayRepport()
        self.control_tournament = ControlTournament()

    def manage_tournament(self):
        """manage the tournament"""
        while True:
            choice = self.tournament_view.display_tournament_menu()
            if choice == "1":

                self.control_tournament.create_tournament()

            elif choice == "2":

                self.control_tournament.continue_last_tournament()

            elif choice == "3":
                self.control_tournament.select_and_continue_tournament()

            elif choice == "4":
                """select and repport a tournament"""
                self.display_repport.select_and_report_tournament()
                break

            elif choice == "5":
                """show list of tournament"""
                self.control_tournament.display_all_tournaments()
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
        self.view = Display()
        self.display_repport = DisplayRepport()
        self.tournament_player = TournamentPlayer(self)

        pass

    def create_tournament(self):
        """
        Create a tournament with the given players.
        """

        tournament_data = self.tournament_view.get_tournament_data()
        tournament = TournamentModel(**tournament_data)
        tournament = self.tournament_manager.id_tournament(tournament)

        self.view.display_table("Player list",
                                [player for player in Player.all()],
                                exclude_headers=["birth_date", "score"])
        players_ids = self.tournament_view.tournament_choose_player()

        tournament = self.tournament_player.add_player(players_ids, tournament)
        self.tournament_manager.save(tournament)
        self.display_repport.display_tournament_info(tournament)
        self.manage_current_round(tournament)

    def display_all_tournaments(self):
        """Display all tournament from the data base"""
        tournaments = self.tournament_manager.load_all_tournament()
        self.view.display_table(
            "Tournament",
            [tournament for tournament in tournaments],
            exclude_headers=["rounds", "players"],
        )

    def continue_last_tournament(self):
        """Continue the last tournament from the database"""
        last_id = self.tournament_manager.get_last_tournament_id()
        if last_id:
            tournament = self.tournament_manager.load_tournament(last_id)
            self.display_repport.display_tournament_info(tournament)
            self.manage_current_round(tournament)
        else:
            self.view.display_message("No tournament found!")

    def select_and_continue_tournament(self):
        """Select a tournament and to continue it"""
        tournaments = self.tournament_manager.load_all_tournament()
        self.view.display_table(
            "Tournament",
            [tournament for tournament in tournaments],
            exclude_headers=["rounds", "players"],
        )

        while True:
            try:
                id = self.view.display_input("Right the number of the id: ")
                tournament = self.tournament_manager.load_tournament(int(id))

                if tournament:
                    self.display_repport.display_tournament_info(tournament)
                    self.manage_current_round(tournament)
                    break

                self.view.display_message("Tournament not found!")
            except ValueError:
                self.view.display_error_input()

    def manage_current_round(self, tournament: TournamentModel):
        """manage round, organise opponent"""

        round_continue = True
        while round_continue:
            if tournament.current_round > int(tournament.number_of_round):
                self.view.display_message(
                    "--- The tournament is already end! ---\n"
                    )
                break
            else:
                choice = self.round_view.manage_round_view()
                if choice != "1":
                    tournament.paused()
                    self.view.display_message(
                        self.tournament_manager.update_tournament(tournament))
                    break

                tournament.resume()

                rounds = None

                try:
                    rounds = tournament.rounds[tournament.current_round - 1]

                except IndexError:
                    pass

                if rounds is None:
                    if tournament.current_round == 1:
                        rd.shuffle(tournament.players)
                    else:
                        self.tournament_player.update_player_scores(tournament)
                        players = tournament.players
                        players.sort(key=lambda x: (x.score), reverse=True)

                    rounds = self.create_round(tournament)

                self.view.get_matches(rounds)

                round_choice = self.manage_score(rounds)

                if "Paused" == round_choice.status:

                    self.paused_tournament(tournament, rounds)

                    break

                tournament.current_round += 1

                round_continue = self.manage_update_tournament(tournament,
                                                               round_choice)

    def manage_update_tournament(self, tournament: TournamentModel,
                                 rounds: RoundModels) -> bool:
        """Manage the update of the tournament after a round."""
        if tournament.current_round > int(tournament.number_of_round):
            self.view.display_message(
                "Tournament has reached the maximum number of rounds"
            )
            tournament.finished()
            print('\ntournament: ', tournament)
            print('\ntournament: ', tournament.rounds)
            tournament.end_date = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S")
            self.manage_update_round(tournament, rounds)
            self.view.display_message(
                f"The tournament: {tournament.name} is finished"
            )
            self.display_repport.repport(tournament)
            return False

        else:
            self.manage_update_round(tournament, rounds)

            self.view.display_message(
                f"Round {tournament.current_round - 1} is finished"
            )
            self.view.display_message(
                "Initialization of the Round "
                f"{tournament.current_round}\n"
            )
            return True

    def paused_tournament(self, tournament: TournamentModel,
                          rounds: RoundModels):
        """Manage the tournament when it is paused."""
        tournament.paused()
        tournament.rounds.append(rounds)
        self.update(tournament)

    def manage_update_round(self, tournament: TournamentModel,
                            rounds: RoundModels):
        """Manage the update of the round."""

        existing_round = next((r for r in
                               tournament.rounds
                               if r.name == rounds.name), None)
        if existing_round:
            if [r for r in tournament.rounds if r.name != rounds.name]:
                tournament.rounds.remove(existing_round)

        tournament.rounds.append(rounds)

        self.update(tournament)

    def update(self, tournament: TournamentModel):
        """Update the tournament."""
        self.view.display_message(
            f"Update of the tournament: {tournament.name}"
            f"{self.tournament_manager.update_tournament(tournament)}")

    def create_round(self,
                     tournament: TournamentModel) -> RoundModels:
        """Creat and built opponnent for the current round"""
        matches = []
        name = f"Round {tournament.current_round}"
        start_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        players = tournament.players.copy()
        while len(players) > 1:
            player_1 = players.pop(0)
            player_2 = players.pop(0)
            match = Match(
                player1_score=TournamentPlayer(player_1),
                player2_score=TournamentPlayer(player_2),
            )

            matches.append(match)

        rounds = RoundModels(matches=matches, start_date=start_date, name=name)
        return rounds

    def manage_score(self, round: RoundModels) -> RoundModels:
        """Add score to players"""
        choice = self.round_view.get_round_choice()

        if choice != "1":
            round.status = "Paused"
            return round

        for pairing in round.matches:
            result = self.round_view.get_match_result(pairing, round.name)

            # Reset the scores
            pairing.player1_score.score = 0.0
            pairing.player2_score.score = 0.0
            if result == "1":

                self.round_view.display_match_result(
                    pairing.player1_score.player.full_name
                    )
                pairing.player1_score.score += 1.0

            elif result == "2":
                self.round_view.display_match_result(
                    pairing.player2_score.player.full_name
                    )
                pairing.player2_score.score += 1.0

            elif result == "0":
                self.round_view.display_match_result(None, is_draw=True)
                pairing.player1_score.score = 0.5
                pairing.player2_score.score += 0.5

            round.end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            round.status = "Finished"
            pairing.end_date = datetime.now()

        return round


class DisplayRepport:
    def __init__(self):
        self.view = Display()
        self.tournament_manager = TournamentManager()
        self.tournament_player = TournamentPlayer(self)

    def select_and_report_tournament(self, repport=None):
        """Select a tournament and report it"""
        tournaments = self.tournament_manager.load_all_tournament()
        repport = True
        while repport:
            self.view.display_table(
                "Tournament",
                [tournament for tournament in tournaments],
                exclude_headers=["rounds", "players"],
            )
            id = self.view.display_input("Right the number of the id: ")
            try:
                tournament = self.tournament_manager.load_tournament(int(id))
                break
            except ValueError as e:
                self.view.display_message(f"{e}")
                continue

        self.repport(tournament)

    def repport(self, tournament: TournamentModel):
        """Fonction to report a tournament"""
        self.view.clear_screen()
        self.tournament_player.update_player_scores(tournament)
        player = sorted(tournament.players,
                        key=lambda
                        x: x.score,
                        reverse=True)

        self.view.display_table(
            "Tournament: ",
            [tournament.to_dict],
            exclude_headers=["rounds", "players"]
        )
        for rounds in tournament.rounds:
            self.view.get_repport(rounds)
        self.view.display_player(player)

    def display_tournament_info(self, tournament: TournamentModel):
        self.view.display_table(
            "Tournament: ",
            [tournament.to_dict],
            exclude_headers=["rounds", "players"]
        )
        self.view.display_table(
            "Player list: ",
            [player.to_dict for player in tournament.players],
            exclude_headers=["score", "birth_date"],
        )
