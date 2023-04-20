from game import Game

def open_game():
    print("Welcome to Pacman for the terminal!")
    print("Please select a mode to play:")
    print("1. Player Input")
    print("2. Run Genetic Algorithm")
    print("3. Run Best Individual")
    #take input from player and run the appropriate function
    mode = input("Enter a number: ")
    if mode == "1":
        start_player_game()
    elif mode == "2":
        start_genetic_game()
    elif mode == "3":
        start_best_game()
    else:
        print("Invalid input. Please try again.")
        open_game()

def start_player_game():
    game = Game()
    print("Starting Player Input Game...")
    print("Controls: 1 = up, 2 = right, 3 = down, 4 = left")
    game.play_game()

if __name__ == "__main__":
    open_game()