from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from datetime import datetime
from tinydb import TinyDB, Query
from chess.models.player_model import Player, PlayerManager
from chess.models.data_manager import ManageData


DB_PATH_PLAYER = "_data/players.json"
DB_PATH_TOURNAMENT = "_data/tournament.json"


@dataclass
class TournamentModel:
    name: str
    place: str
    start_date: str
    description: str
    number_of_round: int
    current_round: int = 1
    _status: str = "In_progress"
    matches: dict[str, Any] = field(default_factory=dict)
    doc_id: Optional[int] = None
    end_date: Optional[str] = None
    _players: List["TournamentPlayer"] = field(default_factory=list)

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
            "status": self.status,
            "players": [player for player in self.players],
            "matches": self.matches,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TournamentModel":
        players = data.get("players", [])
        status = data.get("status")  # Extract status separately
        tournament_data = {k: v for k, v in data.items() if k != "players" and k != "status"}
        tournament = cls(**tournament_data)
        tournament._status = status  # Set status after creating the object
        tournament.players = players
        return tournament


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

    def __init__(self):
        self.manage_data = ManageData()
        self.db = TinyDB(DB_PATH_PLAYER)
        self.db_tournament = self.db.table("tournament")


    def save_tournament(self, tournament: TournamentModel) -> int:
        all_tournament = self.manage_data.get_tournament_list()
        self.highest_doc_id = (
            max([doc.doc_id for doc in all_tournament]) if all_tournament else 0
        )
        self.doc_id = self.highest_doc_id + 1
        tournament.doc_id = self.doc_id
        tournament_dict = tournament.to_dict
        return self.manage_data.save_tournament(tournament_dict)

    def get_all_tournament(self):
        return self.manage_data.get_tournament_list()

    def get_tournament(self, tournament_id: int) -> 'TournamentModel':
        tournament_data = self.manage_data.load_tournament_data(tournament_id)
        tournaments = tournament_data[0]
        if tournaments is None:
            raise ValueError(f"Tournament not found:{tournament_id}")
        return TournamentModel.from_dict(tournaments)
         

    def update(
        self, tournament: TournamentModel, matches: List[Dict[str, Any]]
    ) -> None:
        current_round = tournament.current_round
        round_key = f"Round {current_round}"

        if round_key not in tournament.matches:
            tournament.matches[round_key] = []

        tournament.matches[round_key] = []

        for matche_data in matches:
            player1 = TournamentPlayer.from_dict(matche_data["player1"])
            player2 = TournamentPlayer.from_dict(matche_data["player2"])
            match = Match(
                player1=player1,
                player2=player2,
                start_date=matche_data["start_date"],
                end_date=matche_data["end_"],
            )

            tournament.matches[round_key].append(match.to_dict())
        try:
            return self.manage_data.update_tournament(
                tournament.doc_id, tournament.to_dict
            )
        except Exception as e:
            print(f"fail update tournament: {e}")

    def get_last_tournament_id(self) -> int:
        all_tournament = self.get_all_tournament()
        if not all_tournament:
            raise ValueError("No tournament_found.")
        return max([doc.doc_id for doc in all_tournament])


@dataclass
class TournamentPlayer:
    doc_id: int
    score: float
    first_name: str
    last_name: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "score": self.score,
            "first_name": self.first_name,
            "last_name": self.last_name,

        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TournamentPlayer":
        return cls(**data)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class TournamentPlayerManager:

    def __init__(self):
        self.db = TinyDB(DB_PATH_PLAYER)
        self.db_player = self.db.table("players")
        self.manage_data = ManageData()
        self.player_manager = PlayerManager()
        pass

    def parsed_player_number(self, list_player_number):
        player_number = [int(s) for s in list_player_number.split()]
        return player_number
    
    def add_player(self, player, tournament):
        new_players = self.parsed_player_number(player)
        tournament.players.extend(new_players)
        return tournament

    def extract_player_list(self, tournament):
        """choose player for the tournament"""
        try:
            list_player_number = tournament['players']
            player_list = []
            for player_id in list_player_number:
                player = self.manage_data.get_player(player_id)
                if player:
                    player_list.append(player)

            player_object = []
            for player_data in player_list:
                player_data = Player(
                    first_name=player_data["first_name"],
                    last_name=player_data["last_name"],
                    doc_id=player_data["doc_id"],
                    score=player_data["score"],
                    birth_date=player_data["birth_date"],
                    chess_id=player_data["chess_id"],
                )
                player_object.append(player_data)

            return player_object
        except KeyError:
            raise ValueError("tournament_data must contain a 'player_list' key")

