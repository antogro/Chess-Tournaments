import re



from datetime import datetime


class Player:
    def __init__(self, first_name: str, second_name: str, date_birth: str, player_id: str):
        self.first_name = first_name
        self.second_name = second_name
        self.date_birth = date_birth
        self.player_id = player_id
        