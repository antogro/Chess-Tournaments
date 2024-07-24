import random as rd
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from .data_manager import ManageData
from .player_model import Player
from .table_manager import TableManager
from .tournament_model import TournamentModel, TournamentPlayer


@dataclass
class Match:
    """Class to manage a match between two players"""

    player1: "TournamentPlayer"
    player2: "TournamentPlayer"
    player1_score: float = 0
    player2_score: float = 0
    start_date: datetime = datetime.now()
    end_date: Optional[datetime] = None

    def to_dict(self):
        return {
            "player1": self.player1.to_dict(),
            "player1_score": self.player1_score,
            "player2": self.player2.to_dict(),
            "player2_score": self.player2_score,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Match":
        return cls(
            player1=TournamentPlayer.from_dict(data["player1"]),
            player1_score=data["player1_score"],
            player2=TournamentPlayer.from_dict(data["player2"]),
            player2_score=data["player2_score"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=(
                datetime.fromisoformat(data["end_date"]) if data["end_date"] else None
            )
        )

    def __repr__(self) -> str:
        return (
            f"{self.player1} {self.player1_score}, {self.player2_score} {self.player2}"
        )

    def to_list(self) -> List:
        return [
            [self.player1.doc_id, self.player1_score],
            [self.player2.doc_id, self.player2_score],
            self.start_date.isoformat(),
            self.end_date.isoformat() if self.end_date else None,
        ]
    
    @classmethod
    def from_list(cls, data: List) -> "Match":
        player1_data = {"doc_id": data[0][0], "score": data[0][1]}
        player2_data = {"doc_id": data[1][0], "score": data[1][1]}
        start_date = datetime.fromisoformat(data[2])
        end_date = datetime.fromisoformat(data[3]) if data[3] else None
        return cls(
            player1=TournamentPlayer.from_dict(player1_data),
            player2=TournamentPlayer.from_dict(player2_data),
            player1_score=player1_data["score"],
            player2_score=player2_data["score"],
            start_date=start_date,
            end_date=end_date
        )


@dataclass
class RoundModels:
    name: str
    _start_date: datetime
    _end_date: Optional[datetime] = None
    status: str = "In_progress"
    matches: List[Match] = field(default_factory=list)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if isinstance(value, datetime):
            self._start_date = value
        else:
            raise ValueError("start_date must be a datetime object")

    @property
    def end_date(self) -> Optional[datetime]:
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        if value is None or isinstance(value, datetime):
            self._end_date = value
        else:
            raise ValueError("end_date must be a datetime object or None")

    def __str__(self) -> str:
        msg = f"Round {self.name} - Start: {self.start_date}"
        if self.end_date == "":
            msg += "In progress"
        else:
            msg += f"End: {self.end_date}"
        return msg

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "matches": [match.to_dict() for match in self.matches],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoundModels":
        return cls(
            name=data["name"],
            _start_date=datetime.fromisoformat(data["start_date"]),
            _end_date=(
                datetime.fromisoformat(data["end_date"]) if data["end_date"] else None
            ),
            status=data["status"],
            matches=[Match.from_dict(match_data) for match_data in data["matches"]],
        )


class RoundManager:
    def __init__(self, table_namaner: TableManager, manage_data: ManageData) -> None:
        self.table_manager = table_namaner
        self.manage_data = manage_data

    def mixed_player(self, tournament):

        player_list = tournament._players

        rd.shuffle(player_list)
        tournament.players = player_list

        return tournament.to_dict
    
  
        

    def extract_and_display_round(self, pairings: List[TournamentPlayer]):
        """Extracts and displays the round from the tournament model"""

        readable_pairings = []

        for pairing in pairings:

            pairing_dict = pairing.to_dict()

            readable_pairings.append(pairing_dict)
        table_data = self.format_table_data(readable_pairings)
        print('table_data: ', table_data)
        


        self.table_manager.display_table("Opponent list", table_data)

    def display_pairing_round(self, tournament):
        match = tournament.match
        self.table_manager.display_table("Opponent list", match)

    def format_table_data(self, readable_pairings: List[Dict[str, Any]]) -> List[List[str]]:
        table_data = []
        for pairing in readable_pairings:
            player1_name = f"{pairing['player1']['first_name']} {pairing['player1']['last_name']}"
            player2_name = f"{pairing['player2']['first_name']} {pairing['player2']['last_name']}"
            table_row = [player1_name, player2_name]
            table_data.append(table_row)
        return table_data

        
    def link_player_names(self, matches: List[Match]) -> List[Dict[str, Any]]:
        linked_pairs = []
        for match in matches:
            linked_pairs.append({
                "player1": f"{match.player1.first_name} {match.player1.last_name}",
                "player1_score": match.player1_score,
                "player2": f"{match.player2.first_name} {match.player2.last_name}",
                "player2_score": match.player2_score,
                "start_date": match.start_date.isoformat(),
                "end_date": match.end_date.isoformat() if match.end_date else None,
            })
        return linked_pairs


    # def link_player_names(self, pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        
        # linked_pairs = []
        # for pair in pairs:
        #     linked_pair = {
        #         "player1": f"{pair['player1']['first_name']} {pair['player1']['last_name']}",
        #         "player1_score": pair['player1']['score'],
        #         "player2": f"{pair['player2']['first_name']} {pair['player2']['last_name']}",
        #         "player2_score": pair['player2']['score'],
        #         "start_date": pair['start_date'],
        #         "end_date": pair['end_date']
        #     }
        #     linked_pairs.append(linked_pair)
        # return linked_pairs
        
        # player_dict = {player.doc_id: player for player in players}
        
        # readable_pairings = []
        
        # # Accédez à chaque clé de round et ses appariements
        # for round_key, matches in pairings.items():
        #     for match in matches:
        #         try:
        #             player1_info, player2_info, start_date, end_date = match
        #             player1_id, player1_score = player1_info
        #             player2_id, player2_score = player2_info
                    
        #             player1 = player_dict.get(player1_id)
        #             player2 = player_dict.get(player2_id)


        #             readable_pairings.append({
        #                     "player1": player1,
        #                     "player1_score": player1_score,
        #                     "player2": player2,
        #                     "player2_score": player2_score,
        #                     "start_date": start_date,
        #                     "end_date": end_date,
        #             })
                   

        #         except ValueError as e:
        #             print(f"Error processing match data: {e}")
        
        # return readable_pairings