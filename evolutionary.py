from copy import deepcopy
from random import choice, random, choices, randint

### EVOLUTIONARY ALGORITHM ###


def evolve(puzzle, mutation_rate, trunc_rate, population_size):
    bests = []
    best_ind = None
    population = generate_population(puzzle, population_size)
    population_fitness = fitness_population(population)

    for generation in range(NUMBER_GENERATION):
        # select parents for reproduction
        mating_pool = selection_population(
            population, population_fitness, trunc_rate)

        # create children
        offspring_population = crossover_population(mating_pool)

        # mutate children
        population = mutate_population(
            offspring_population, puzzle, mutation_rate)

        # calculate fitness of the population
        population_fitness = fitness_population(population)

        # implement elitism so best candidate always stays without mutation
        if best_ind:
            worst, worst_fitness = bottom_population(
                population, population_fitness)
            population.remove(worst)
            population.append(best_ind)

        # recalculate fitness
        population_fitness = fitness_population(population)

        # find best candidate
        best_ind, best_fit = top_population(population, population_fitness)
        bests.append(best_fit)

        # check its a winner or not
        if(best_fit == 0):
            print("\nGeneration: ", str(generation))
            print("SOLVED")
            pretty_print(best_ind)
            break

        # if get stuck in a local minima/maxima, decrease the mutation and increase the truncation rate to improve diversity
        if(bests.count(best_fit) > 10):
            mutation_rate = 0.0001
            trunc_rate = 0.4

        print("\nGeneration: ", str(generation),
              "\nTiles Out Of Place: ", str(best_fit))
        pretty_print(best_ind)

### POPULATION-LEVEL OPERATORS ###


def generate_population(puzzle, population_size):
    return [generate(puzzle) for _ in range(population_size)]


def fitness_population(population):
    return [fitness(individual) for individual in population]


def selection_population(population, fitness_population, trunc_rate):
    sorted_population = sorted(zip(population, fitness_population),
                               key=lambda individual_fitness: individual_fitness[1])

    return [individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * trunc_rate)]]


def roulette_choose(population):
    return(choices(population=population, weights=[fitness(candidate) for candidate in population], k=2))


def crossover_population(population):
    crossed_population = []
    for _ in range(int(POPULATION_SIZE/2)):
        child1, child2 = crossover(choice(population), choice(population))
        crossed_population.append(child1)
        crossed_population.append(child2)
    return crossed_population


def mutate_population(population, puzzle, mutation_rate):
    return [mutate(individual, puzzle, mutation_rate) for individual in population]


def top_population(population, fitness_population):
    return sorted(zip(population, fitness_population), key=lambda individual_fitness: individual_fitness[1])[0]


def bottom_population(population, fitness_population):
    return sorted(zip(population, fitness_population), key=lambda individual_fitness: individual_fitness[1])[-1]

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###


def generate(puzzle):
    candidate = deepcopy(puzzle)
    for i in range(PUZZLE_SIZE):
        if(candidate[i] == 0):
            candidate[i] = choice(digits)
    return candidate


def fitness(individual):

    rows = [individual[i:i + 9] for i in range(0, len(individual), 9)]
    row_fitness = sum(9 - len(set(row)) for row in rows)

    columns = [individual[i::9] for i in range(0, 9)]
    column_fitness = sum(9 - len(set(column)) for column in columns)

    boxes = []
    for i in range(0, 7, 3):
        boxes.append(rows[i][0: 3] + rows[i+1][0: 3] + rows[i+2][0: 3])
        boxes.append(rows[i][3: 6] + rows[i+1][3: 6] + rows[i+2][3: 6])
        boxes.append(rows[i][6: 9] + rows[i+1][6: 9] + rows[i+2][6: 9])
    box_fitness = sum(9 - len(set(box)) for box in boxes)

    fitness = row_fitness + column_fitness + box_fitness
    return fitness


def crossover(individual1, individual2):
    child1 = []
    child2 = []

    for parent_pair in zip(individual1, individual2):
        choice = randint(0, 1)
        child1.append(parent_pair[choice])
        child2.append(parent_pair[abs(choice-1)])

    return child1, child2


def mutate(individual, puzzle, mutation_rate):
    return [(choice(digits) if random() < mutation_rate and puzzle[x] == 0 else individual[x]) for x in range(len(individual))]


def pretty_print(individual):
    rows = [individual[i:i + 9] for i in range(0, len(individual), 9)]
    for row in rows:
        print(row)

### PARAMETER VALUES ###


PUZZLE_SIZE = 81
NUMBER_GENERATION = 10000000000
POPULATION_SIZE = 10000
TRUNCATION_RATE = 0.04
MUTATION_RATE = 0.01

digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
sudoku1 = [3, 0, 0, 0, 0, 5, 0, 4, 7, 0, 0, 6, 0, 4, 2, 0, 0, 1, 0, 0, 0, 0, 0, 7, 8, 9, 0, 0, 5, 0, 0, 1, 6, 0, 0, 2, 0, 0, 3,
           0, 0, 0, 0, 0, 4, 8, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 5, 6, 0, 8, 7, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 6, 0, 0]
sudoku2 = [0, 0, 2, 0, 0, 0, 6, 3, 4, 1, 0, 6, 0, 0, 0, 5, 8, 0, 0, 0, 7, 3, 0, 0, 2, 9, 0, 0, 8, 5, 0, 0, 1, 0, 0, 6, 0, 0, 0,
           7, 5, 0, 0, 2, 3, 0, 0, 3, 0, 0, 0, 0, 5, 0, 3, 1, 4, 0, 0, 2, 0, 0, 0, 0, 0, 9, 0, 8, 0, 4, 0, 0, 7, 2, 0, 0, 4, 0, 0, 0, 9]
sudoku3 = [0, 0, 4, 0, 1, 0, 0, 6, 0, 9, 0, 0, 0, 0, 0, 0, 3, 0, 0, 5, 0, 7, 9, 6, 0, 0, 0, 0, 0, 2, 5, 0, 4, 9, 0, 0, 0, 8, 3,
           0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 7, 0, 0, 0, 9, 0, 3, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0]


### EVOLVE ###

evolve(sudoku1, MUTATION_RATE, TRUNCATION_RATE, POPULATION_SIZE)

# for 10000 population, start with mutation rate 0.01 then change to 0.0001, start with trunc rate at 0.04 then change to 0.4

# for 1000 population, set strunc rate to 0.1

# for 100 population, set trunc rate to 0.2

# for 10 population, set trunc rate to 0.4
