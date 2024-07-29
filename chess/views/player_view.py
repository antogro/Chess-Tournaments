

class PlayerView:

    def display_player_menu(self):
        print("1. Create a new player")
        print("2. Players list")
        print("3. Select and modify player")
        print("Q. Exit")
        menu_player = input("Right your choose number: ")

        return menu_player

    def chess_id_construc(self):
        """construc the chess id code"""

        while True:
            chess_id = input("Right your chess id: ")

            if not chess_id:
                print("N/A")
                continue

            if len(chess_id) != 7:
                print("Invalid ID: must be 7 charactere")
                continue

            chess_id_letter = chess_id[:2]
            chess_id_number = chess_id[2:]

            if not chess_id_letter.isalpha():
                print("Invalid ID: must start by 2 letters")
                continue

            if not chess_id_number.isdigit():
                print("Invalid ID: must end by 5 number")
                continue

            return f"{chess_id_letter.upper()}{chess_id_number}"

    def get_player_data(self):
        print("\n--- Add a new player ---")
        self.first_name = input("First Name: ")
        self.last_name = input("Last Name: ")
        self.birth_date = input("birth date (DD/MM/YYYY) : ")
        self.chess_id = self.chess_id_construc()
        self.score = 0

        player_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "chess_id": self.chess_id,
            "score": self.score,
        }
        return player_data

    def display_new_player(self, player_add):
        print(f"\n ---- New player created: {player_add.first_name} ----\n")

    
