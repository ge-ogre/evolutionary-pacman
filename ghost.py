# ghosts will always move in the same direction until they hit a wall
# then they will choose a new direction based on the player's position

import random

class Ghost:
    def __init__(self, type):
        self.type = type
        self.viable_directions = []
        self.direction = None
        self.currently_standing = "0"

    def update_direction(self, cur_map, player_row, player_column, ghost_row, ghost_column):
        # then we check which directions are viable
        viable_directions = self.get_viable_directions(cur_map, ghost_row, ghost_column)
        if viable_directions != self.viable_directions or self.direction == None:
            # if the viable directions have changed, we choose a new direction
            if self.type == "d": # clyde
                self.direction = random.choice(viable_directions)
            elif self.type == "a": # blinky-ish
                self.direction = self.get_closest_direction(player_row, player_column, ghost_row, ghost_column, viable_directions)
            self.viable_directions = viable_directions

    def get_viable_directions(self, map, ghost_row, ghost_column):
        viable_directions = []
        row = ghost_row
        column = ghost_column

        # 1 = N, 2 = E, 3 = S, 4 = W
        if map[row - 1][column] != "#":
            viable_directions.append("1")
        if map[row][column + 1] != "#":
            viable_directions.append("2")
        if map[row + 1][column] != "#":
            viable_directions.append("3")
        if map[row][column - 1] != "#":
            viable_directions.append("4")
        return viable_directions

    # def get_closest_direction(self, player_row, player_column, ghost_row, ghost_column, viable_directions):
    #     if viable_directions == []:
    #         return 0
    #     else:
    #         # sorts list of viable directions, takes the one with the lowest distance
    #         closest_direction = sorted(viable_directions, key = lambda direction: self.get_distance(player_row, player_column, ghost_row, ghost_column, direction), reverse=True)[0]
    #         print(sorted(viable_directions, key = lambda direction: self.get_distance(player_row, player_column, ghost_row, ghost_column, direction), reverse=True))
    #         return closest_direction
    
    def get_closest_direction(self, player_row, player_column, ghost_row, ghost_column, viable_directions):
        if not viable_directions:
            return 0

        horizontal_diff = player_column - ghost_column
        vertical_diff = player_row - ghost_row

        if abs(horizontal_diff) > abs(vertical_diff):
            if horizontal_diff > 0 and "2" in viable_directions:
                return "2"  # move right
            elif horizontal_diff < 0 and "4" in viable_directions:
                return "4"  # move left
        else:
            if vertical_diff > 0 and "3" in viable_directions:
                return "3"  # move down
            elif vertical_diff < 0 and "1" in viable_directions:
                return "1"  # move up

        # If the preferred direction is not in viable_directions, choose a random direction
        return random.choice(viable_directions)


    def get_distance(self, player_row, player_column, ghost_row, ghost_column, direction):
        row = ghost_row
        column = ghost_column
        if direction == "1":
            return abs(player_row - 1 - row) + abs(player_column - column)
        elif direction == "2":
            return abs(player_row - row) + abs(player_column + 1 - column)
        elif direction == "3":
            return abs(player_row + 1 - row) + abs(player_column - column)
        elif direction == "4":
            return abs(player_row - row) + abs(player_column - 1 - column)
        else:
            return 0