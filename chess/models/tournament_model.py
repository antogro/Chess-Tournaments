from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from chess.models.player_model import Player
from .table_manager import TableManager
from datetime import datetime
from .._database._database import db_tournament


@dataclass
class TournamentModel:
    name: str
    place: str
    start_date: str
    description: str
    number_of_round: int
    current_round: int = 1
    _status: str = "In_progress"
    rounds: list = None
    doc_id: Optional[int] = None
    end_date: Optional[str] = None
    _players: List["TournamentPlayer"] = field(default_factory=list)

    def __post_init(self):
        self.rounds = []

    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_round": self.number_of_round,
            "current_round": self.current_round,
            "status": self._status,
            "players": [player.player.doc_id for player in self.players],
            "rounds": [round.to_dict for round in self.rounds]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TournamentModel":
        players = [Player.get_player(id=doc_id) for doc_id in data["players"]]
        tournament_data = {
        "doc_id": data.get("doc_id"),
        "name": data.get("name"),
        "place": data.get("place"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "description": data.get("description"),
        "number_of_round": data.get("number_of_round"),
        "current_round": data.get("current_round"),
        "_status": data.get("status"),
        "_players": players,
        "rounds": [round.from_dict(match) for match in data.get("rounds", [])]
    }
        return cls(**tournament_data)

    @property
    def players(self) -> List["TournamentPlayer"]:
        return self._players

    @players.setter
    def players(self, value: List["TournamentPlayer"]):
        self._players = value

    @property
    def status(self):
        return self._status

    @status.setter
    def set_status(self, value):
        if value in ["In_progress", "Paused", "Finished"]:
            self._status = value
        else:
            raise ValueError("Invalid status")

    def add_player(self, player: "TournamentPlayer"):
        if player not in self.players:
            self.players.append(player)
        else:
            raise ValueError("Player already exists in the tournament")

    def next_round(self):
        if self.current_round < self.number_of_round:
            self.current_round += 1
        else:
            raise ValueError("Tournament has already reached its final round")

    def resume(self):
        self.set_status = "In_progress"
        

    def paused(self):
        self.set_status = "Paused"

    def finished(self):
        self.set_status = "Finished"


class TournamentManager:
    table: TableManager = db_tournament
    def id_tournament(self, tournament: TournamentModel) -> int:
        all_tournament = self.table.load_all()
        self.doc_id  = (max([doc.doc_id for doc in all_tournament]) if all_tournament else 0)+ 1
        tournament.doc_id = self.doc_id
        return tournament

    def save(self, tournament: TournamentModel):
        return self.table.save(tournament.to_dict)

    def load_all_tournament(self):
        return self.table.load_all()
    
    def update(self, data: TournamentModel, id):
        return self.table.update(data.to_dict, id)

    def load_tournament(self, tournament_id: int) -> 'TournamentModel':
        tournament_data = self.table.load_from_id(tournament_id)
        if tournament_data is None:
            raise ValueError(f"Tournament not found:{tournament_id}")
        return TournamentModel.from_dict(tournament_data)
         

    def update_tournament(self, tournament: TournamentModel) -> None:
        if not tournament.doc_id:
            raise ValueError("Cannot update without doc_id!")
        try:
            tournament_dict = tournament.to_dict
            id = tournament.doc_id
            result = self.table.update(tournament_dict, id)
            if result:
                print("Success to update")
        except Exception as e:
            raise ValueError(f"Error updating tournament: {e}")

    def get_last_tournament_id(self) -> int:
        all_tournament = self.load_all_tournament()
        if not all_tournament:
            raise ValueError("No tournament_found.")
        return max([doc.doc_id for doc in all_tournament])


@dataclass
class TournamentPlayer():
    player: Player
    score: float = 0

    def __repr__(self) -> str:
        return f"{self.player}"
        

    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "player": self.player.to_dict,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TournamentPlayer":
        player = Player.from_dict(data["player"])
        return cls(player = player, score=data['score'])

    def __str__(self) -> str:
        return f"{self.player.first_name} {self.player.last_name}"

    def add_player(self, players_number, tournament: TournamentModel) -> TournamentModel:
        new_players = [int(s) for s in players_number.split()]
        for new_player in new_players:
            player_data = Player.get_player(id=int(new_player))
            if player_data:
                tournament_player = TournamentPlayer(player_data)
                tournament.players.append(tournament_player)

        return tournament


@dataclass
class Match:
    """Class to manage a match between two players"""

    player1_score: TournamentPlayer
    player2_score: TournamentPlayer
    start_date: datetime = datetime.now()
    end_date: Optional[datetime] = None

    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "player1_score": self.player1_score.to_dict,
            "player2_score": self.player2_score.to_dict,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Match":
        return cls(
            player1_score=TournamentPlayer.from_dict(data["player1"]),
            player2_score=TournamentPlayer.from_dict(data["player2"]),
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=(
                datetime.fromisoformat(data["end_date"]) if data["end_date"] else None
            )
        )

    def __repr__(self) -> str:
        return (f"[[{self.player1_score.player.doc_id}, {self.player1_score.score}], [{self.player2_score.player.doc_id}, {self.player2_score.score}]]")


@dataclass
class RoundModels:
    name: str
    matches: List[Match]
    start_date: str = str(datetime.today)
    end_date: str = None
    status: str = "In_progress"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date if self.end_date else None,
            "status": self.status,
            "matches": [match.to_dict for match in self.matches],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoundModels":
        matches = [Match.from_dict(match_data) for match_data in data["matches"]]
        return cls(
            name=data["name"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            status=data["status"],
            matches=matches
            )

    

