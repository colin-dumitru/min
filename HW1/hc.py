from common import *
from random import randint

MAX_ITERATIONS = 1
SAMPLES = 100
NEIGHBOURHOOD_SPREAD = 10
PRINT_ITERATIONS = True

improve = None
test_func = None

def simple_improve(neighbours):
    best = None
    best_neighbor = None

    for neighbour in neighbours:
        current_value = test_func.test(neighbour)

        if not best or current_value < best:
            best = current_value
            best_neighbor = neighbour

    return best_neighbor


def random_binary():
    return [
        randint(0, 1)
        for i in range(0, PRECISION)
    ]


def random_selection():
    return [
        random_binary()
        for i in range(0, test_func.variables)
    ]


def random_neighbor(values):
    rand_value = [randint(0, 1) for i in range(0, NEIGHBOURHOOD_SPREAD)]

    if randint(0, 1):
        return to_bin(max(to_int(values) - to_int(rand_value), 0), PRECISION)
    else:
        return to_bin(min(to_int(values) + to_int(rand_value), 2**PRECISION), PRECISION)


def neighbourhood(values):
    return [
        [random_neighbor(values[v]) for v in range(0, test_func.variables)]
        for i in range(0, SAMPLES)
    ]


def same_solution(v1, v2):
    for tuple in zip(v1, v2):
        for value in zip(tuple[0], tuple[1]):
            if value[0] != value[1]:
                return False

    return True


def print_solution(values):
    if not PRINT_ITERATIONS:
        return

    print("%f: (%s)" % (test_func.test(values), ",".join([
        str(to_real(value, test_func.min, test_func.max))
        for value in values
    ])))


def do_hc():
    iterations = 0
    solutions = []

    while iterations < MAX_ITERATIONS:
        print("---------------------- Iteration %d -------------------------" % iterations)

        current = random_selection()
        local = False

        while not local:
            neighbors = neighbourhood(current)
            improved = improve(neighbors)

            if test_func.test(improved) > test_func.test(current):
                local = True
            else:
                local = False
                current = improved

            print_solution(current)

        iterations += 1
        solutions.append(current)

    return solutions


def run_test(func):
    global test_func

    test_func = func
    solutions = do_hc()

    print("Solutions: (%s)" % ",".join([str(round(func.test(solution), 4)) for solution in solutions]))
    print("Best: %f" % min([round(func.test(solution), 4) for solution in solutions]))


if __name__ == '__main__':
    improve = simple_improve

    #run_test(SixHumpCamelBack())
    #run_test(Rosenbrock())
    run_test(Griewangk())
    #run_test(Rastrigin())

