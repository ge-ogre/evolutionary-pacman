import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from game import Game

# Preproccess the game state
def preprocess_game_state(map):
    game_state = []

    for row in map:
        for item in row:
            if item == "_":
                game_state.append(0)
            elif item == "#":
                game_state.append(1)
            elif item == "0":
                game_state.append(2)
            elif item == "1":
                game_state.append(3)
            elif item == "a":
                game_state.append(4)
            elif item == "b":
                game_state.append(5)

    # Normalize the game state
    game_state = np.array(game_state)
    game_state = game_state / max(game_state)

    return game_state

# Create a neural network model
def create_agent():
    model = Sequential()
    model.add(Dense(32, input_dim=9, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    return model

# Evaluate the agent's performance
def evaluate_agent(agent):
    game = Game()
    play_agent(game, agent)
    return game.score

def play_agent(game, agent):
    print("Starting Agent Game...")
    while(not game.is_over):
        game.display_game()
        direction = get_next_move_agent(agent, game.map)
        game.move_player(direction)
        game.is_over = game.check_is_over()

def get_next_move_agent(agent, map):
    game_state = preprocess_game_state(map)
    action_list = agent.predict(np.array([game_state]))
    prediction = np.argmax(action_list) + 1
    return prediction

# Perform uniform crossover
def crossover(agent1, agent2):
    offspring1 = create_agent()
    offspring2 = create_agent()

    for i in range(len(agent1.layers)):
        layer_weights1 = agent1.layers[i].get_weights()
        layer_weights2 = agent2.layers[i].get_weights()

        for j in range(len(layer_weights1)):
            mask = np.random.rand(*layer_weights1[j].shape) < 0.5
            offspring_weights1 = np.where(mask, layer_weights1[j], layer_weights2[j])
            offspring_weights2 = np.where(mask, layer_weights2[j], layer_weights1[j])

            offspring1.layers[i].set_weights([offspring_weights1])
            offspring2.layers[i].set_weights([offspring_weights2])

    return offspring1, offspring2

# Mutate the agent
def mutate(agent, mutation_rate):
    for i, layer in enumerate(agent.layers):
        weights = layer.get_weights()
        new_weights = []

        for weight in weights:
            mutation = (np.random.randn(*weight.shape) * mutation_rate)
            new_weights.append(weight + mutation)

        agent.layers[i].set_weights(new_weights)

# Roulette selection
def roulette_selection(agents, fitnesses):
    total_fitness = sum(fitnesses)
    pick = np.random.rand() * total_fitness
    current = 0

    for i, fitness in enumerate(fitnesses):
        current += fitness
        if current > pick:
            return agents[i]

# Run the genetic algorithm
def run_genetic_algorithm():
    population_size = 50
    num_generations = 100
    mutation_rate = 0.01

    # Create initial population
    population = [create_agent() for _ in range(population_size)]

    for gen in range(num_generations):
        print(f"Generation {gen + 1}")

        # Evaluate fitness
        fitnesses = [evaluate_agent(agent) for agent in population]

        # Select parents and perform crossover and mutation
        new_population = []

        for _ in range(population_size // 2):
            parent1 = roulette_selection(population, fitnesses)
            parent2 = roulette_selection(population, fitnesses)
            offspring1, offspring2 = crossover(parent1, parent2)

            mutate(offspring1, mutation_rate)
            mutate(offspring2, mutation_rate)

            new_population.append(offspring1)
            new_population.append(offspring2)

        population = new_population

    # Get the best agent from the final population
    best_agent = population[np.argmax(fitnesses)]

    return best_agent
