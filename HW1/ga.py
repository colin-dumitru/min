from common import *
from random import random
from random import randint
from random import shuffle

ITERATIONS = 100
SELECTION_SIZE = 0.6
MUTATION_PROBABILITY = 0.2
GENE_MUTATION_PROBABILITY = 0.1
COMBINATION_POINTS = 10

test_func = None
print_evolution = False


def cum_sum(l):
    cumulative = []

    for i in range(0, len(l)):
        if i == 0:
            cumulative.append(l[i])
        else:
            cumulative.append(cumulative[i-1] + l[i])

    return cumulative


# ------------------- Selection -----------------------------
def select(cumulative, population):
    rand = random()

    for i in range(0, len(population)):
        if cumulative[i] > rand:
            return population[i]

    return population[-1]


def selection(population):
    eval = [test_func.fitness(p) for p in population]
    min_fitness = min(eval)
    eval = [v - min_fitness for v in eval]

    total_fitness = sum(eval) + 0.0000001
    probabilities = [fitness / total_fitness for fitness in eval]
    cumulative = cum_sum(probabilities)

    return [select(cumulative, population) for i in range(0, int(len(population) * SELECTION_SIZE))]

# ------------------- Mutation -----------------------------
def mutate_gene(gene):
    if random() > GENE_MUTATION_PROBABILITY:
        return gene

    return randint(0,1)


def mutate_chromosome(chromosome):
    if random() > MUTATION_PROBABILITY:
        return chromosome

    return [mutate_gene(g) for g in chromosome]


def mutation(population):
    return [
        mutate_chromosome(chromosome)
        for chromosome in population
    ]

# ------------------- Re-combine -----------------------------
def either(val1, val2):
    if randint(0,1):
        return val1
    else:
        return val2


def combine(chromosome1, chromosome2):
    indexes = sorted([randint(0, len(chromosome1)) for i in range(0, COMBINATION_POINTS)])
    segments = []

    for i in range(0, len(indexes)):
        if i == 0:
            # add first segment
            segments.append(either(chromosome1, chromosome2)[0:indexes[i]])
        else:
            segments.append(either(chromosome1, chromosome2)[indexes[i-1]:indexes[i]])

    # add last segment
    segments.append(either(chromosome1, chromosome2)[indexes[-1]:])

    return sum(segments, [])


def random_chromosome(population):
    return population[randint(0, len(population) - 1)]


def recombine(population, count):
    return population + [
        combine(random_chromosome(population), random_chromosome(population))
        for i in range(0, count)
    ]


# ------------------- Iteration -----------------------------
def best_chromosome(population):
    best = None
    best_score = None

    for p in population:
        score = test_func.fitness(p)

        if not best_score or score > best_score:
            best = p
            best_score = score

    return best


def print_chromosome(chromosome):
    values = partition(chromosome, test_func.variables)

    print("optimal: %f (%s)" % (
        test_func.test(values),
        ",".join([str(to_real(v, test_func.min, test_func.max)) for v in values])
    ))


def get_optimum_solution(population):
    for i in range(0, ITERATIONS):
        selected = selection(population)
        mutated = mutation(selected)
        recombined = recombine(mutated, int(len(population) * round(1 - SELECTION_SIZE,2)))

        shuffle(recombined)
        population = recombined

        print_chromosome(best_chromosome(population)) if print_evolution else 0

    return population


def improve_ga(neighbours):
    population = [sum(n, []) for n in neighbours]
    final_population = get_optimum_solution(population)

    best = best_chromosome(final_population)
    return partition(best, test_func.variables)


def do_test():
    initial_population = [
        [randint(0, 1) for j in range(0, PRECISION * test_func.variables)]
        for i in range(0, 100)
    ]

    get_optimum_solution(initial_population)


def main():
    global test_func
    global print_evolution

    print_evolution = True

    test_func = SixHumpCamelBack()
    # test_func = Griewangk()
    # test_func = Rastrigin()
    # test_func = Rosenbrock()

    do_test()

if __name__ == '__main__':
    main()

