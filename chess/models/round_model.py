import random as rd


class RamdomPlayer:
    def __init__(self):

        pass

    # def round_set(self, tournament_data):

    def mixed_player(self, tournament_data):
        if isinstance(tournament_data, list):

            if len(tournament_data) > 0:
                tournament_data = tournament_data[0]

        assert isinstance(tournament_data, dict)
        player_list = tournament_data.get("player_list")
        assert isinstance(player_list, list)

        rd.shuffle(player_list)
        round_data = {"match": player_list}

        return round_data

    def get_versus_player(self, player_list):
        round_data = {}
        player_round = []

        for i in range(0, len(player_list), 2):
            if i + 1 < len(player_list):

                player_round.append([player_list[i], player_list[i + 1]])
            else:
                player_round.append([player_list[i], None])

        round_data = {"match": player_round}

        return round_data


class RoundModel:
    def __init__(self, player_list):
        self.player_list = player_list

    # def roun_data_funct(self):
    #     round_data = {
    #         "round_number": ,
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
