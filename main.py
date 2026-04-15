from game import Game
from ga_algo import run_genetic_algorithm
import maps
from graphics import PygameRenderer

def open_game():
    print("Welcome to Evolutionary Pacman!")
    print("Please select a mode to play:")
    print("1. Player Input")
    print("2. Run Genetic Algorithm")
    print("3. Run Best Individual")    
    
    mode = input("Enter a number: ")
    
    use_gui = False
    if mode in ["1", "3"]:
        print("Use graphical mode? (y/n)")
        use_gui = input().lower() == 'y'
    
    print("Select a map:")
    print("1. Small Map")
    print("2. Line Map")
    print("3. Symmetry Map")
    selected_map_choice = ""
    while (selected_map_choice != "1" and selected_map_choice != "2" and selected_map_choice != "3"):
        selected_map_choice = input("Select a map: ")
    
    selected_map = maps.create_map(selected_map_choice)
    
    renderer = None
    if use_gui:
        renderer = PygameRenderer(len(selected_map["map"][0]), len(selected_map["map"]))

    if mode == "1":
        start_player_game(selected_map, renderer)
    elif mode == "2":
        start_genetic_game(selected_map)
    elif mode == "3":
        print("Run Best Individual is not fully implemented yet.")
        # start_best_game()
    else:
        print("Invalid input. Please try again.")
        open_game()

def start_player_game(selected_map, renderer=None):
    game = Game(selected_map)
    if not renderer:
        print("Controls: 1 = up, 2 = right, 3 = down, 4 = left")
    game.play_game(renderer)

def start_genetic_game(selected_map):
    run_genetic_algorithm(selected_map)

if __name__ == "__main__":
    open_game()
