from game import Game
from ga_algo import run_genetic_algorithm
import maps

def open_game():
    print("Welcome to Pacman for the terminal!")
    print("Please select a mode to play:")
    print("1. Player Input")
    print("2. Run Genetic Algorithm")
    print("3. Run Best Individual")    
    #take input from player and run the appropriate function
    mode = input("Enter a number: ")
    print("Select a map:")
    print("1. Small Map")
    print("2. Line Map")
    print("3. Symmetry Map")
    selected_map = ""
    while (selected_map != "1" and selected_map != "2" and selected_map != "3"):
        selected_map = input("Select a map: ")
    selected_map = maps.create_map(selected_map)
    if mode == "1":
        start_player_game(selected_map)
    elif mode == "2":
        start_genetic_game(selected_map)
    elif mode == "3":
        start_best_game()
    else:
        print("Invalid input. Please try again.")
        open_game()

def start_player_game(selected_map):
    game = Game(selected_map)
    print("Starting Player Input Game...")
    print("Controls: 1 = up, 2 = right, 3 = down, 4 = left")
    game.play_game()

def start_genetic_game(selected_map):
    run_genetic_algorithm(selected_map)

if __name__ == "__main__":
    open_game()