from common import *
from random import random
from random import randint

import hc

ITERATIONS = 10
SELECTION_SIZE = 0.6
MUTATION_PROBABILITY = 0.1
GENE_MUTATION_PROBABILITY = 0.1
COMBINATION_POINTS = 10

test_func = None

def cumsum(l):
    cumulative = []

    for i in range(0, len(l)):
        if i == 0:
            cumulative.append(l[i])
        else:
            cumulative.append(l[i-1] + l[i])

    return cumulative

# ------------------- Selection -----------------------------
def select(cumulative, population):
    rand = random()

    for i in range(0, len(population)):
        if cumulative[i] > rand:
            return population[i]

    return population[-1]


def selection(population):
    eval = [ test_func.fitness(p) for p in population ]
    total_fitness = sum(eval)
    probabilities = [fitness / total_fitness for fitness in eval]
    cumulative = cumsum(probabilities)

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
            segments.append(either(chromosome1, chromosome2)[indexes[i-1], indexes[i]])

    # add last segment
    segments.append(either(chromosome1, chromosome2)[indexes[-1]:])

    return sum(indexes, [])

def random_chromosome(population):
    return population[randint(0, len(population) - 1)]

def recombine(population, count):
    return population + [
        combine(random_chromosome(population), random_chromosome(population))
        for i in range(0, count)
    ]


# ------------------- Iteration -----------------------------
def get_optimum_solution(population):
    for i in range(0, ITERATIONS):
        selected = selection(population)
        mutated = mutation(selected)
        recombined = recombine(mutated, len(population) * (1 - SELECTION_SIZE))

        population = recombined


def main():
    test_func = SixHumpCamelBack()

if __name__ == '__main__':
    main()

