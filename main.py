import constants
from random import sample, shuffle, random
from typing import List, Tuple, Any, Union
import time

Genome = List[int]
Population = List[Genome]

mutation_rate = constants.MUTATION_RATE
mutation_decrease_step = mutation_rate / constants.MAX_GENERATIONS

def create_population(size = constants.DEFAULT_POPULATION_SIZE) -> Population:
    return [
        sample(range(0, constants.CHESS_BOARD_SIZE), constants.CHESS_BOARD_SIZE) for i in range(0, size)
    ]

def optimize_genome(genome: Genome) -> Genome:
    occurrences: List[Tuple] = []
    for i in range(0, constants.CHESS_BOARD_SIZE):
        occurrences.append((i, genome.count(i)))
    zeros: List[Tuple] = []
    more_than_one: List[Tuple] = []
    for item in occurrences:
        if item[1] == 0:
            zeros.append(item)
        elif item[1] > 1:
            more_than_one.append(item)
    shuffle(zeros)
    for i in range(0, len(more_than_one)):
        genome[genome.index(more_than_one[i][0])] = zeros[i][0]
    return genome

def calc_fitness(genome: Genome) -> float:
    cost = 0
    for i in range(0, len(genome)):
        col = genome[i]
        for j in range(i + 1, len(genome)):
            col2 = genome[j]
            gradient = abs((j - i) / (col2 - col))
            if gradient == 1:
                cost += 1
    return 1 / (cost + 1)

def crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    child1 = a[:constants.CHESS_BOARD_SIZE // 2]
    child1.extend(b[constants.CHESS_BOARD_SIZE // 2:])
    child2 = b[:constants.CHESS_BOARD_SIZE // 2]
    child2.extend(a[constants.CHESS_BOARD_SIZE // 2:])
    return optimize_genome(child1), optimize_genome(child2)

def mutate_population(population: Population) -> Population:
    for item in population:
        rand = random()
        if rand <= mutation_rate:
            positions = sample(range(0, constants.CHESS_BOARD_SIZE), 2)
            item[positions[0]], item[positions[1]] = item[positions[1]], item[positions[0]]
    return population

def find_solution() -> Union[Genome, None]:
    global mutation_rate
    def consider_second_value_in_sort(elem):
        return elem[1]
    population = create_population()
    max_fitness = 0
    best_so_far: Union[Genome, None] = None
    for generation in range(1, constants.MAX_GENERATIONS + 1):
        population_fitness: List[Tuple[Genome, float]] = []
        for genome in population:
            fitness = calc_fitness(genome)
            population_fitness.append((genome, fitness))
            if fitness == 1:
                return genome
            if fitness > max_fitness:
                max_fitness = fitness
                best_so_far = genome
        population_fitness.sort(key=consider_second_value_in_sort, reverse=True)
        population = [pf[0] for pf in population_fitness]
        for i in range(0, len(population) // 2):
            rand = random()
            if rand <= constants.CROSS_OVER_POSSIBILITY:
                positions = [i * 2, i * 2 + 1]
                population[positions[0]], population[positions[1]] = crossover(population[positions[0]],
                                                                               population[positions[1]])
        population = mutate_population(population)
        mutation_rate -= mutation_decrease_step
        if best_so_far is not None:
            position = sample(range(0, len(population)), 1)
            population[position[0]] = best_so_far
        print(f'went from generation {generation} to {generation + 1}')
    return None

def print_chess_board(genome: Genome):
    board = [
        [
            0 for k in range(0, constants.CHESS_BOARD_SIZE)
        ] for l in range(0, constants.CHESS_BOARD_SIZE)
    ]
    for i in range(0, len(genome)):
        board[i][genome[i]] = 1
    for row in board:
        print('')
        for col in row:
            print(col if col == 0 else u"\u265B", end="    ")
        print('')
    print('')

start = time.time()
a = find_solution()
end = time.time()
print_chess_board(a)
print(f'it took {end - start}s to find a solution')

