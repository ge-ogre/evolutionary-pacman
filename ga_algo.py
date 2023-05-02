import random
import numpy as np
from game import Game
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential

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
def create_agent(map):
    input_dim = len(map["map"]) * len(map["map"][0])

    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dense(16, activation='relu'))
    # one output node for each direction
    model.add(Dense(4, activation='softmax'))
    return model

# Evaluate the agent's performance
def evaluate_agent(agent, map, generation):
    game = Game({k: v for (k, v) in map.items()})
    max_turns = generation * 4
    play_agent(game, agent, max_turns)
    return game.score

def play_agent(game, agent, max_turns):
    print("Starting Agent Game...")
    turns = 0
    while not game.is_over and turns < max_turns:
        direction = get_next_move_agent(agent, game.map)
        print(direction)
        game.move_player(str(int(direction)))
        game.move_ghosts()
        game.display_game()
        game.is_over = game.check_is_over()
        turns += 1

def get_next_move_agent(agent, map):
    game_state = preprocess_game_state(map)
    action_probabilities = agent.predict(np.array([game_state]))[0]

    # Normalize the probabilities
    normalized_probs = action_probabilities / np.sum(action_probabilities)

    # Implement roulette wheel selection
    random_val = random.random()
    cum_sum = 0
    for index, prob in enumerate(normalized_probs):
        cum_sum += prob
        if cum_sum > random_val:
            return index + 1

    # Fallback to the max value in case the loop doesn't return
    return np.argmax(action_probabilities) + 1

# Perform uniform crossover
def crossover(agent1, agent2, map):
    offspring1 = create_agent(map)
    offspring2 = create_agent(map)

    for i in range(len(agent1.layers)):
        layer_weights1 = agent1.layers[i].get_weights()
        layer_weights2 = agent2.layers[i].get_weights()

        offspring_weights1 = []
        offspring_weights2 = []

        for j in range(len(layer_weights1)):
            mask = np.random.rand(*layer_weights1[j].shape) < 0.5
            offspring_weight1 = np.where(mask, layer_weights1[j], layer_weights2[j])
            offspring_weight2 = np.where(mask, layer_weights2[j], layer_weights1[j])

            offspring_weights1.append(offspring_weight1)
            offspring_weights2.append(offspring_weight2)

        offspring1.layers[i].set_weights(offspring_weights1)
        offspring2.layers[i].set_weights(offspring_weights2)

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

    # Fallback to return the last agent in the list
    return agents[-1]

def run_genetic_algorithm(map):
    population_size = 25
    num_generations = 50
    mutation_rate = 0.01
    elitism_rate = 0.1 

    # Create initial population
    population = [create_agent(map) for _ in range(population_size)]

    average_fitnesses = []  # Store the average fitness of each generation
    best_fitnesses = []  # Store the best fitness of each generation

    for gen in range(num_generations):
        print(f"Generation {gen + 1}")

        fitnesses = []
        for agent in range(len(population)):
            print("Individual", agent)
            fitnesses.append(evaluate_agent(population[agent], map, gen + 1))

        average_fitness = sum(fitnesses) / len(fitnesses)
        average_fitnesses.append(average_fitness)

        sorted_indices = np.argsort(fitnesses)[::-1]
        num_elites = int(elitism_rate * population_size)

        new_population = [population[i] for i in sorted_indices[:num_elites]]
        best_fitnesses.append(fitnesses[sorted_indices[0]])
        print("Best fitness for generation:", fitnesses[sorted_indices[0]])

        while len(new_population) < population_size:
            parent_indices = random.sample(range(population_size), 2)
            parent1 = population[parent_indices[0]]
            parent2 = population[parent_indices[1]]
            offspring1, offspring2 = crossover(parent1, parent2, map)

            mutate(offspring1, mutation_rate)
            mutate(offspring2, mutation_rate)

            group = [parent1, parent2, offspring1, offspring2]
            group_fitnesses = [fitnesses[parent_indices[0]], fitnesses[parent_indices[1]],
                               evaluate_agent(offspring1, map, gen+1), evaluate_agent(offspring2, map, gen+1)]

            selected1 = roulette_selection(group, group_fitnesses)
            selected2 = roulette_selection(group, group_fitnesses)

            new_population.append(selected1)
            new_population.append(selected2)

        population = new_population

    best_agent = population[np.argmax(fitnesses)]

    # Plot the average fitness over generations
    plt.plot(average_fitnesses, label="Average Fitness")
    plt.plot(best_fitnesses, label="Best Fitness")
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over Generations')
    plt.show()

    return best_agent