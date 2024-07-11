from chess.views.round_view import RoundView
from chess.models.table_manager import TableManager
from chess.models.data_manager import ManageData
from chess.models.round_model import RamdomPlayer


class RoundControl:
    def __init__(self, round_number, round_time_start, round_time_end):
        self.round_number = round_number
        self.round_time_start = round_time_start
        self.round_time_end = round_time_end

        self.table_manager = TableManager()
        self.data_manager = ManageData()
        self.round_model = RamdomPlayer()
        self.round_tournament = RoundTournament()
        self.round_view = RoundView()

    def round(self, tournament_data, tournament_id):

        while True:
            choice = self.round_view.manage_round_view()
            if choice == "1":
                round_id = self.round_tournament.first_round_tournament(tournament_data)
                self.round_tournament.second_round_tournament(round_id, tournament_data, tournament_id)
                continue
            elif choice == "2":
                break


class RoundTournament:
    def __init__(self):
        self.table_manager = TableManager()
        self.data_manager = ManageData()
        self.round_model = RamdomPlayer()
        self.round_view = RoundView()

    def first_round_tournament(self, tournament_data):
        print("tournament data name:", tournament_data["name"])
        print("type tournemantr data", type(tournament_data))
        self.table_manager.display_tournament_table(tournament_data)
        round_data = self.round_model.mixed_player(tournament_data)
        self.round_view.manage_round(round_data)   
        return self.data_manager.save_round(round_data)

    def second_round_tournament(self, round_id, tournement_data, tournament_id):
        


