from math import cos
from math import sqrt
from math import pi

class TestFunction():
    def fitness(self, x):
        return self.test(partition(x, self.variables))

class Griewangk:
    def __init__(self):
        TestFunction.__init__(self)

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
        TestFunction.__init__(self)

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
        TestFunction.__init__(self)

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
        TestFunction.__init__(self)

        self.max = 2.0
        self.min = -2.0
        self.variables = 2

    def test(self, x):
        x = [to_real(xi) for xi in x]
        x1 = x[0]
        x2 = x[1]

        return (4 - 2.1 * (x1**2) + (x1**4.0 / 3.0)) * (x1**2) + x1 * x2 + (-4 + 4 * x2**2) * x2**2


def partition(l, parts):
    partition_len = int(len(l) / parts)
    return [l[i * partition_len: (i + 1) * partition_len] for i in range(0, parts)]