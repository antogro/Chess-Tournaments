
class RoundControl:
    def __init__(self, round_number, round_time_start, round_time_end)
        self.round_number = round_number
        self.round_time_start = round_time_start
        self.round_time_end = round_time_end
        self.round_time = round_time_end - round_time_start

    def start_round(self):
        
        print("Round " + str(self.round_number) + " started at " + str(self.round_time)