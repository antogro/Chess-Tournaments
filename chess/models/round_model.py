import random as rd
from datetime import datetime


class RoundModels:
    def __init__(self):
        pass

    def creat_match_data(self, player1, player2, start_time=None, end_time=None):
        if start_time is None:
            start_time = datetime.now().isoformat()

        return {
            "player1": {"doc_id": player1["doc_id"], "score": player1["score"]},
            "player2": {"doc_id": player2["doc_id"], "score": player2["score"]},
            "start_time": start_time,
            "end_time": end_time,
        }

    def have_played_before(self, player1, player2, tournament_data):
        if "matches" not in tournament_data:
            return False
        for match in tournament_data["matches"]:
            if (
                match["player1"]["doc_id"] == player1["doc_id"]
                and match["player2"]["doc_id"] == match["player2"]["doc_id"]
            ) or (
                match["player1"]["doc_id"] == player2["doc_id"]
                and match["player2"]["doc_id"] == player1["doc_id"]
            ):
                return True
        return False

    def creat_pairing_first_round(self, player_list):
        pairings = []
        for i in range(0, len(player_list), 2):
            try:
                player1 = player_list[i]
                player2 = player_list[i + 1]
                pairing = self.creat_match_data(player1, player2)
                pairings.append(pairing)
            except IndexError:
                print("No enought player, one player don't have oppoent")
        return pairings

    def mixed_player(self, tournament_data):
        if isinstance(tournament_data, list):

            if len(tournament_data) > 0:
                tournament_data = tournament_data[0]

        assert isinstance(tournament_data, dict)
        player_list = tournament_data.get("player_list")
        assert isinstance(player_list, list)

        rd.shuffle(player_list)
        tournament_data = {"player_list": player_list}

        return tournament_data

    # def get_versus_player(self, tournament_data):
    #     player_round = []

    #     for i in range(0, len(player_list), 2):
    #         if i + 1 < len(player_list):

    #             player_round.append([player_list[i], player_list[i + 1]])
    #         else:
    #             player_round.append([player_list[i], None])

    #     tournament_data = {"match": player_round}

    #     return round_data


# class RoundControl:
#     def __init__(self):
#         pass


# class RoundModel:
#     def __init__(self, player_list):
#         self.player_list = player_list

#     # def roun_data_funct(self):
#     #     round_data = {
#     #         "round_number": ,
#         "status": "in_progess",
#         "match":
#     }

# def start_round(self, player_list):
#     for player in player_list:

# # def get_stronger_versus_stronger(self, player_round):
# #     stronger_player = []
# #     player_rank = player_round.get("rank")

# #     for i in range(0, len(player_round)):
# #         for i > player_rank :
