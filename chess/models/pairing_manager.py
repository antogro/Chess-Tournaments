
from chess.models.round_model import Match
import random
from datetime import datetime
from typing import List

from chess.models.tournament_model import TournamentModel, TournamentPlayer


class PairingManager:
    def __init__(self, pairing):
        self.pairing = pairing

    @staticmethod
    def creat_pairing_first_round(players: List[TournamentPlayer]) -> List[Match]:
        pairings = []
        random.shuffle(players)
        for i in range(1, len(players), 2):
            if i + 1 < len(players):
                player1 = players[i]
                player2 = players[i+1]
                match = Match(
                    player1=player1,
                    player1_score=player1.score,
                    player2=player2,
                    player2_score=player2.score,
                    
                    start_date=datetime.now()
                )
                pairings.append(match)
            else:
                print(f"Warning: Player {players[i].first_name} {players[i].last_name} doesn't have an opponent in this round.")
        return pairings





    @staticmethod
    def have_played_before(player1: TournamentPlayer,
                           player2: TournamentPlayer,
                           tournament: TournamentModel
                           ) -> bool:
        for matche in tournament.match:
            if (
                matche.player1 == player1
                and matche.player2 == player2
            ) or (
                matche.player1 == player2
                and matche.player2 == player1
            ):
                return True
        return False
    
    @staticmethod
    def creat_pairing_next_round(tournament: TournamentModel) -> List[Match]:

        sorted_players = sorted(tournament._player_list, key=lambda x: (-x.score, x.doc_id))
        pairings = []
        used_players = set()

        for i in range(0, len(sorted_players) - 1, 2):
            player1 = sorted_players[i]
            player2 = sorted_players[i + 1]

            if (
                player1.doc_id not in used_players
                and player2.doc_id not in used_players
            ):
                pairing = PairingManager.creat_match_data(player1, player2, tournament)
                pairings.append(pairing)
                used_players.add(player1.doc_id)
                used_players.add(player2.doc_id)

        # Gérer le cas d'un nombre impair de joueurs
        if len(sorted_players) % 2 != 0:
            last_player = sorted_players[-1]
            if last_player.doc_id not in used_players:
                print(
                    f"Player {last_player.first_name} {last_player.last_name} doesn't have an opponent this round."
                )

 
        return pairings
    
    def creat_match_data(
        self, player1, player2, start_time=None, end_time=None
    ):

        if start_time is None:
            start_time = datetime.now()
            formated_start_time = start_time.strftime("%d-%m-%Y %H:%M:%S")
        if isinstance(tournament_data, list):
            tournament_data = tournament_data[0] if tournament_data else {}

        return {
            "player1": {
                "doc_id": player1.doc_id,
                "score": player1.score,
                "first_name": player1.first_name,
                "last_name": player1.last_name,
            },
            "player2": {
                "doc_id": player2.doc_id,
                "score": player2.score,
                "first_name": player2.first_name,
                "last_name": player2.last_name,
            },
            "start_time": formated_start_time,
            "end_time": end_time,
        }