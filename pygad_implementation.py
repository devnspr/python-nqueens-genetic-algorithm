import constants
import pygad
from typing import List

Genome = List[int]

def calc_fitness(genome: Genome, idx) -> float:
    cost = 0
    for i in range(0, len(genome)):
        col = genome[i]
        for j in range(i + 1, len(genome)):
            col2 = genome[j]
            gradient = abs((j - i) / (col2 - col))
            if gradient == 1:
                cost += 1
    return 1 / (cost + 1)

fitness_function = calc_fitness

num_generations = constants.MAX_GENERATIONS
num_parents_mating = 2
sol_per_pop = 3
num_genes = constants.CHESS_BOARD_SIZE
init_range_low = -2
init_range_high = 5
parent_selection_type = "sss"
keep_parents = 1
crossover_type = "two_points"
mutation_type = "random"
mutation_percent_genes = constants.MUTATION_RATE * 100

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       gene_type=int,
                       gene_space=[
                           range(0, constants.CHESS_BOARD_SIZE) for i in range(0, constants.CHESS_BOARD_SIZE)
                       ],
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       allow_duplicate_genes=False)

ga_instance.run()

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

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print_chess_board(solution)
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
