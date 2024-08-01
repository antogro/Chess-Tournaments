from dataclasses import dataclass, field
import builtins
from typing import Any, List, Dict, Optional, Union
from chess.models.player_model import Player
from .table_manager import TableManager
from datetime import datetime
from .._database._database import db_tournament

@dataclass
class RoundModels:
    """Class to manage the rounds of a tournament"""
    name: str
    matches: List["Match"]
    start_date: str 
    end_date: Optional[str] = None
    status: str = "In_progress"

    @property
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object RoundModels to a dictionary"""
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "matches": [match.to_dict for match in self.matches],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoundModels":
        """Convert a dictionary to a RoundModels object"""
        matches = [Match.from_dict(match_data) for match_data in data["matches"]]
        return cls(
            name=data["name"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            status=data["status"],
            matches=matches
            )


@dataclass
class TournamentModel(Player):
    """Class to manage the tournament"""

    name: str
    place: str
    start_date: str
    description: str
    number_of_round: int
    current_round: int = 1
    _status: str = "In_progress"
    doc_id: Optional[int] = None
    end_date: Optional[str] = None
    rounds: List[RoundModels] = field(default_factory=list)
    _players: List["TournamentPlayer"] = field(default_factory=list)

    @property
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object TournamentModel to a dictionary"""
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
            "players": [player.player.doc_id for player in self._players],
            "rounds": [round.to_dict for round in self.rounds]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TournamentModel":
        """Convert a dictionary to a TournamentModel object"""
        players = [TournamentPlayer(Player.get_player(doc_id)) for doc_id in data["players"]]
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
        "rounds": [RoundModels.from_dict(match) for match in data.get("rounds", [])]
    }
        return cls(**tournament_data)

    @property
    def players(self) -> List["TournamentPlayer"]:
        """Get the list of players in the tournament"""
        return self._players

    @players.setter
    def players(self, value: List["TournamentPlayer"]):
        """Set the list of players in the tournament"""
        self._players = value

    @property
    def status(self):
        """Get the status of the tournament"""
        return self._status

    @status.setter
    def set_status(self, value):
        """Set the status of the tournament"""
        if value in ["In_progress", "Paused", "Finished"]:
            self._status = value
        else:
            raise ValueError("Invalid status")

    def add_player(self, player: "TournamentPlayer"):
        """Add a player to the tournament"""
        if player not in self.players:
            self.players.append(player)
        else:
            raise ValueError("Player already exists in the tournament")

    def resume(self):
        """Set the status as Resumed"""
        self.set_status = "In_progress"

    def paused(self):
        """set the status as Paused"""
        self.set_status = "Paused"

    def finished(self):
        """set the status as Finished"""
        self.set_status = "Finished"


class TournamentManager:
    """Class to manage the information of a tournament"""
    table: TableManager = db_tournament

    def id_tournament(self, tournament: TournamentModel) -> TournamentModel:
        """Get and set the id of the tournament"""
        all_tournament = self.table.load_all()
        self.doc_id  = (max([doc.doc_id for doc in all_tournament]) if all_tournament else 0)+ 1
        tournament.doc_id = self.doc_id
        return tournament

    def save(self, tournament: TournamentModel) -> int:
        """Save the tournament in the database"""
        return self.table.save(tournament.to_dict)

    def load_all_tournament(self) -> List[TournamentModel]:
        """Load all the tournament from the database"""
        return self.table.load_all()
    
    def update(self, data, id) -> int:
        """Update the tournament in the database"""
        return self.table.update(data, id)

    def load_tournament(self, tournament_id: int) -> TournamentModel:
        """Load a tournament from the database with an ID"""
        tournament_data = self.table.load_from_id(tournament_id)
        if tournament_data is None:
            raise ValueError(f"Tournament not found:{tournament_id}")
        return TournamentModel.from_dict(tournament_data)

    def update_tournament(self, tournament: TournamentModel) -> None:
        """Update the tournament in the database"""
        if not tournament.doc_id:
            raise ValueError("Cannot update without doc_id!")
        try:
            tournament_dict = tournament.to_dict
            id = tournament.doc_id
            for key, value in tournament_dict.items():
                if isinstance(value, datetime):
                    print(f"Converting {key} to string: {value.isoformat()}")
                    tournament_dict[key] = value.isoformat()
            result = self.table.update(tournament_dict, id)
            if result:
                print("Success to update")
        except Exception as e:
            raise ValueError(f"Error updating tournament: {e}")

    def get_last_tournament_id(self) -> int:
        """Get the last tournament id"""
        all_tournament = self.load_all_tournament()
        if not all_tournament:
            raise ValueError("No tournament_found.")
        return max([doc.doc_id for doc in all_tournament])

@dataclass
class TournamentPlayer():
    player: Player
    score: float = 0

    @property
    def to_dict(self) -> Dict[str, Any]:
        """Convert the TournamentPlayer object to a dictionary"""
        return {self.player}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TournamentPlayer":
        """Convert a dictionary to a TournamentPlayer object"""
        return cls(data[0])

    def __str__(self) -> str:
        return f"{self.player.first_name} {self.player.last_name}"

    def add_player(self, players_number, tournament: TournamentModel) -> TournamentModel:
        """Add and set player object to the tournament"""
        new_players = [int(s) for s in players_numbers.split()]
        for new_player in new_players:
            player_data = Player.get_player(id=int(new_player))
            if player_data:
                tournament_player = TournamentPlayer(player_data)
                tournament.players.append(tournament_player)

        return tournament

    def update_player_scores(self, tournament: TournamentModel):
        # Reset all scores to 0
        for player in tournament.players:
            player.score = 0

        # Create a dictionary for faster player lookup
        player_dict = {player.player.doc_id: player for player in tournament.players}

        for tournament_round in tournament.rounds:  # Renamed 'round' to 'tournament_round'
            for match in tournament_round.matches:
                player1 = player_dict.get(match.player1_score.player.doc_id)
                player2 = player_dict.get(match.player2_score.player.doc_id)

                if player1 and player2:
                    player1.score += match.player1_score.score
                    player2.score += match.player2_score.score

        # Round scores to 1 decimal place using the built-in round function
        for player in tournament.players:
            player.score = builtins.round(player.score, 1)


@dataclass
class Match:
    """Class to manage a match between two players"""

    player1_score: TournamentPlayer
    player2_score: TournamentPlayer
    start_date: str = field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    end_date: Optional[datetime] = None

    def __repr__(self) -> str:
        return (f"[[{self.player1_score.player.doc_id}, {self.player1_score.player.score}], [{self.player2_score.player.doc_id}, {self.player2_score.player.score}]]")

    @property
    def to_dict(self):
        """Convert a Match object to a dictionary"""
        start_date = self.start_date.strftime("%d-%m-%Y %H:%M:%S") if isinstance(self.start_date, datetime) else self.start_date
        end_date = self.end_date.strftime("%d-%m-%Y %H:%M:%S") if isinstance(self.end_date, datetime) else self.end_date

        return [
            [self.player1_score.player.doc_id, self.player1_score.score],
            [self.player2_score.player.doc_id, self.player2_score.score],
            start_date,
            end_date
            ]

    @classmethod
    def from_dict(cls, data: List[List[Union[int, float]]]) -> "Match":
        """Convert a dictionary to a Match object"""
        player1 = TournamentPlayer(Player.get_player(data[0][0]), score=data[0][1])
        player2 = TournamentPlayer(Player.get_player(data[1][0]), score=data[1][1])
        start_date = datetime.strptime(data[2], "%d-%m-%Y %H:%M:%S")  
        end_date = datetime.strptime(data[3], "%d-%m-%Y %H:%M:%S") if data[3] else None 
        return cls(player1_score=player1, player2_score=player2, start_date=start_date, end_date=end_date)

    def format_data(self, data: "Match"):
        """Format data for a match"""
        return [[
             data.player1_score.player, data.player1_score.score],
             [data.player2_score.player, data.player2_score.score], 
             data.start_date, data.end_date
        ]




    

