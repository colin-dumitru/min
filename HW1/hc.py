from random import randint
from math import cos
from math import sqrt
from math import pi

MAX_ITERATIONS = 1
SAMPLES = 100
PRECISION = 16
PRECISION_DEC = pow(2, PRECISION)
NEIGHBOURHOOD_SPREAD = 10
PRINT_ITERATIONS = True

improve = None
test_func = None


class Griewangk:
    def __init__(self):
        self.max = 600.0
        self.min = -600.0
        self.variables = 3

    def test(self, x):
        x = [to_real(xi) for xi in x]

        s = sum([(xi * xi) / 4000.0 for xi in x])

        p = 1

        for i in range(0, self.variables):
            p *= cos(x[i] / sqrt(i + 1))

        return s - p + 1


class Rastrigin:
    def __init__(self):
        self.max = 5.12
        self.min = -5.12
        self.variables = 3

    def test(self, x):
        x = [to_real(xi) for xi in x]

        return 10.0 * self.variables + sum([
            xi * xi - 10.0 * cos(2.0 * pi * xi)
            for xi in x
        ])

class Rosenbrock:
    def __init__(self):
        self.max = 2.048
        self.min = -2.048
        self.variables = 3

    def test(self, x):
        x = [to_real(xi) for xi in x]
        sum = 0.0

        for i in range(0, self.variables - 1):
            sum += 100.0 * pow(x[i + 1] - pow(x[i], 2), 2) + pow(1 - x[i], 2)

        return sum

class SixHumpCamelBack:
    def __init__(self):
        self.max = 2.0
        self.min = -2.0
        self.variables = 2

    def test(self, x):
        x = [to_real(xi) for xi in x]
        x1 = x[0]
        x2 = x[1]

        return (4 - 2.1 * (x1**2) + (x1**4.0 / 3.0)) * (x1**2) + x1 * x2 + (-4 + 4 * x2**2) * x2**2


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


def to_int(value):
    return int(''.join([str(b) for b in value]), 2)


def to_bin(value):
    return [int(c) for c in bin(value)[2:].rjust(PRECISION, '0')]


def to_real(value):
    max = test_func.max
    min = test_func.min

    int_val = to_int(value)

    return min + (((max - min) * int_val) / PRECISION_DEC)


def random_neighbor(values):
    rand_value = [randint(0, 1) for i in range(0, NEIGHBOURHOOD_SPREAD)]

    if randint(0, 1):
        return to_bin(max(to_int(values) - to_int(rand_value), 0))
    else:
        return to_bin(min(to_int(values) + to_int(rand_value), PRECISION_DEC))


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
        str(to_real(value))
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

