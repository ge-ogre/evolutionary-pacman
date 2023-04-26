import random


class Game:
    def __init__(self):
        self.map = self.create_map()
        self.score = 0
        self.is_over = False

    def create_map(self):
            # _ = empty space
            # # = wall
            # 0 = pellet
            # 1 = player
            # a = ghost1
            # b = ghost2
            # c = ghost3
            # d = ghost4
        map = [
            # ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            # ['#', '1', '0', '0', '0', '0', '0', '0', '0', '#'],
            # ['#', '#', '#', '#', '#', '#', '0', '0', '0', '#'],
            # ['#', '0', '0', '0', '0', '0', '0', '0', '0', '#'],
            # ['#', '0', '0', '0', '#', '#', '#', '#', '#', '#'],
            # ['#', '0', '0', '0', '0', '0', '0', 'd', '0', '#'],
            # ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
            ["#", "1", "0", "0", "0", "0", "0", "0", "0", "#"]
        ]
        return map
    
    def get_thing_position(self, thing):
        for row in range(len(self.map)):
            for column in range(len(self.map[row])):
                if self.map[row][column] == thing:
                    return (row, column)
        

    def move_thing(self, thing_type, thing_row, thing_column, direction):
        if thing_type == "player":
            replace = "_"
        else:
            replace = "0"

        # 1 = N, 2 = E, 3 = S, 4 = W
        if direction == "1" and self.map[thing_row - 1][thing_column] != "#":
            # move up
            if self.map[thing_row - 1][thing_column] == "0" and thing_type == "player":
                self.score += 3
            self.map[thing_row][thing_column] = replace
            self.map[thing_row - 1][thing_column] = "1"

        elif direction == "2" and self.map[thing_row][thing_column + 1] != "#":
            # move right
            if self.map[thing_row][thing_column + 1] == "0" and thing_type == "player":
                self.score += 3
            self.map[thing_row][thing_column] = replace
            self.map[thing_row][thing_column + 1] = "1"

        elif direction == "3" and self.map[thing_row + 1][thing_column] != "#":
            # move down
            if self.map[thing_row + 1][thing_column] == "0" and thing_type == "player":
                self.score += 3
            self.map[thing_row][thing_column] = replace
            self.map[thing_row + 1][thing_column] = "1"

        elif direction == "4" and self.map[thing_row][thing_column - 1] != "#":
            # move left
            if self.map[thing_row][thing_column - 1] == "0" and thing_type == "player":
                self.score += 3
            self.map[thing_row][thing_column] = replace
            self.map[thing_row][thing_column - 1] = "1"
        else:
            # error code
            return(420)


    def move_player(self, direction):
        # first we find the player
        player_row, player_column = self.get_thing_position("1")
        # then we move the player
        if self.move_thing("player", player_row, player_column, direction) == 420:
            print("Invalid move. Please try again.")
        else:
            pass

        self.score -= 1
        self.is_over = self.check_is_over()

    def move_ghosts(self):
        for ghost in ["a", "b", "c", "d"]:
            # a = blinky
            if ghost == "a":
                # blinky tends to move directly at pacman
                pass

            # b = inky
            elif ghost == "b":
                # inky tends to move between blinky and pacman
                pass

            # c = pinky
            elif ghost == "c":
                # pinky tends to move towards the space 2 spaces ahead of pacman
                pass

            # d = clyde
            elif ghost == "d":
                # clyde tends to move randomly
                row, col = self.get_thing_position("d")
                print(self.map[row][col])
                direction = random.randint(1, 4)
                while (self.move_thing("ghost", row, col, direction) == 420):
                    direction = random.randint(1, 4)
                self.move_thing("ghost", row, col, direction)

    def check_is_over(self):
        # check if there are any pellets left
        for row in self.map:
            for column in row:
                if column == "0":
                    return False
        self.display_score()
        return True

    def display_game(self):
        for row in self.map:
            print(row)
    
    def display_score(self):
        print(f"Your score was: {self.score}")

    def play_game(self):
        print("Starting Player Input Game...")
        while(not self.is_over):
            self.display_game()
            direction = input("Enter a direction: ")
            self.move_player(direction)
            #self.move_ghosts()
            self.is_over = self.check_is_over()