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
        self.view = Display()
        self.tournament_player = TournamentPlayer(self)

        pass

    def create_tournament(self):
        """
        Create a new tournament, add players,
        save it, and start managing rounds.
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

        self.view.display_table(
            "Tournament: ", [tournament.to_dict],
            exclude_headers=["rounds", "players"]
        )
        self.view.display_table(
            "Player list: ",
            [player.to_dict for player in tournament.players],
            exclude_headers=["score", "birth_date"],
        )
        self.manage_round(tournament)

    def display_all_tournament(self):
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
            self.view.display_table(
                "Tournament: ",
                [tournament.to_dict],
                exclude_headers=["rounds", "players"],
            )
            self.view.display_player(
                [player for player in tournament.players],
                exclude_headers=["Score"])
            self.manage_round(tournament)
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
                    self.view.display_table(
                        "Tournament: ",
                        [tournament.to_dict],
                        exclude_headers=["rounds", "players"],
                    )
                    self.view.display_player(
                        [player for player in tournament.players],
                        exclude_headers=["score", "birth_date"],
                    )
                    self.manage_round(tournament)
                    break

                self.view.display_message("Tournament not found!")
            except ValueError:
                self.view.display_error_input()

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
        self.tournament_player.update_player_scores(tournament)
        player = sorted(tournament.players,
                        key=lambda x: x.score,
                        reverse=True)
        self.view.display_table(
            "Tournament: ", [tournament.to_dict],
            exclude_headers=["rounds", "players"]
        )
        for rounds in tournament.rounds:
            self.view.get_repport(rounds)
        self.view.display_player(player)

    def manage_round(self, tournament: TournamentModel):
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
                    rounds = tournament.rounds[tournament.current_round]
                except IndexError:
                    return rounds

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

                if round_choice == "2":
                    tournament.paused()
                    tournament.rounds.append(rounds)
                    self.view.display_message(
                        self.tournament_manager.update_tournament(tournament))
                    break
                else:
                    tournament.rounds.append(round_choice)

                if tournament.current_round >= int(tournament.number_of_round):
                    self.view.display_message(
                        "Tournament has reached the maximum number of rounds"
                    )
                    round_continue = False
                    tournament.finished()
                    tournament.end_date = datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S")
                    self.view.display_message(
                        self.tournament_manager.update_tournament(tournament))
                    self.view.display_message(
                        f"The tournament: {tournament.name} is finished"
                    )
                    self.repport(tournament)

                else:
                    tournament.current_round += 1
                    self.view.display_message(
                        self.tournament_manager.update_tournament(tournament))
                    self.view.display_message(
                        f"Round {tournament.current_round - 1} is finished"
                    )
                    self.view.display_message(
                        "Initialization of the round"
                        f"{tournament.current_round}\n"
                    )

    def create_round(self, tournament: TournamentModel) -> RoundModels:
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

    def manage_score(self, round: RoundModels):
        """Add score to players"""
        choice = self.round_view.get_round_choice()

        if choice != "1":
            return "2"

        for pairing in round.matches:
            result = self.round_view.get_match_result(pairing, round.name)

            # Reset the scores
            pairing.player1_score.score = 0.0
            pairing.player2_score.score = 0.0

            if result == "1":
                pairing.player1_score.score += 1.0
                self.round_view.display_match_result(
                    pairing.player2_score.player.full_name
                    )

            elif result == "2":
                pairing.player2_score.score += 1.0
                self.round_view.display_match_result(
                    pairing.player2_score.player.full_name
                    )

            elif result == "0":
                self.round_view.display_match_result(None, is_draw=True)
                pairing.player1_score.score = 0.5
                pairing.player2_score.score += 0.5

            round.end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            round.status = "Finished"
            pairing.end_date = datetime.now()

        return round
