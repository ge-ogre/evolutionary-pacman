import random
from ghost import Ghost


class Game:
    def __init__(self, map): 
        self.map = [x for x in { k:v for (k,v) in map.items() }["map"]]
        self.score = 0
        self.is_over = False
        self.ghosts = []
        self.pellet_worth = 3
        self.time_penalty = 1
        for ghost in { k:v for (k,v) in map.items() }["ghosts"]:
            self.ghosts.append(Ghost(ghost))

    def move_thing(self, thing_type, thing_row, thing_column, direction):
        if thing_type == "1":
            replace = "_"
        else:
            replace = ""

        # 1 = N, 2 = E, 3 = S, 4 = W
        if direction == "1" and thing_row > 0 and self.map[thing_row - 1][thing_column] != "#":
            # move up
            # first, we add points for score if the player eats a pellet
            if self.map[thing_row - 1][thing_column] == "0" and thing_type == "1":
                self.score += self.pellet_worth
            # then we must check what to replace the thing with
            # if player, we always replace with empty space
            # if ghost, we replace with whatever it was standing on
            if thing_type != "1":
                ghost = self.get_ghost(thing_type)
                replace = ghost.currently_standing
                ghost.currently_standing = self.map[thing_row - 1][thing_column]
            self.map[thing_row][thing_column] = replace
            # then we move the thing
            self.map[thing_row - 1][thing_column] = thing_type
            # then, return the position of the thing
            return (thing_row, thing_column)
        elif direction == "2" and self.map[thing_row][thing_column + 1] != "#":
            # move right
            if self.map[thing_row][thing_column + 1] == "0" and thing_type == "1":
                self.score += self.pellet_worth
            if thing_type != "1":
                ghost = self.get_ghost(thing_type)
                replace = ghost.currently_standing
                ghost.currently_standing = self.map[thing_row][thing_column + 1]
            self.map[thing_row][thing_column] = replace
            self.map[thing_row][thing_column + 1] = thing_type
            return (thing_row, thing_column)
        elif direction == "3" and self.map[thing_row + 1][thing_column] != "#":
            # move down
            if self.map[thing_row + 1][thing_column] == "0" and thing_type == "1":
                self.score += self.pellet_worth
            if thing_type != "1":
                ghost = self.get_ghost(thing_type)
                replace = ghost.currently_standing
                ghost.currently_standing = self.map[thing_row + 1][thing_column]
            self.map[thing_row][thing_column] = replace
            self.map[thing_row + 1][thing_column] = thing_type
            return (thing_row, thing_column)
        elif direction == "4" and self.map[thing_row][thing_column - 1] != "#":
            # move left
            if self.map[thing_row][thing_column - 1] == "0" and thing_type == "1":
                self.score += self.pellet_worth
            if thing_type != "1":
                ghost = self.get_ghost(thing_type)
                replace = ghost.currently_standing
                ghost.currently_standing = self.map[thing_row][thing_column - 1]
            self.map[thing_row][thing_column] = replace
            self.map[thing_row][thing_column - 1] = thing_type
            return (thing_row, thing_column)
        else:
            # error code
            return(420)

    def move_player(self, direction):
        # first we find the player
        player_row, player_column = self.get_thing_position("1")
        # then we move the player
        if self.move_thing("1", player_row, player_column, direction) == 420:
            #print("Invalid move. Please try again.")
            self.is_over = True
        self.score -= self.time_penalty

    def move_ghosts(self):
        player_row, player_column = self.get_thing_position("1")
        for ghost in self.ghosts:
            ghost_row, ghost_column = self.get_thing_position(ghost.type)
            ghost.update_direction(self.map, player_row, player_column, ghost_row, ghost_column)
            # print("ghost direction: " + ghost.direction)
            # print("ghost viable directions: " + str(ghost.viable_directions))
            # print("ghost position: " + str(ghost_row) + ", " + str(ghost_column))
            ghost_row, ghost_column = self.move_thing(ghost.type, ghost_row, ghost_column, ghost.direction)
            print(ghost.currently_standing)

    def get_thing_position(self, thing):
        for row in range(len(self.map)):
            for column in range(len(self.map[row])):
                if self.map[row][column] == thing:
                    return (row, column)

    def get_ghost(self, type):
        for ghost in self.ghosts:
            if ghost.type == type:
                return ghost

    def check_is_over(self):
        if self.is_over: 
            self.display_score()
            return True
        # check if any ghosts are currenlty on the player
        for ghost in self.ghosts:
            if ghost.currently_standing == "1":
                self.display_score()
                return True
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
        self.display_game()
        while(not self.is_over):
            direction = input("Enter a direction: ")
            self.move_player(direction)
            self.move_ghosts()
            self.display_game()
            self.is_over = self.check_is_over()