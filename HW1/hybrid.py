__author__ = 'colin'

from common import *
import hc
import ga


def run_test(func):
    hc.test_func = func
    ga.test_func = func

    solutions = hc.do_hc()

    print("Solutions: (%s)" % ",".join([str(round(func.test(solution), 4)) for solution in solutions]))
    print("Best: %f" % min([round(func.test(solution), 4) for solution in solutions]))


def main():
    hc.improve = ga.improve_ga

    run_test(SixHumpCamelBack())
    #run_test(Rosenbrock())
    #run_test(Griewangk())
    #run_test(Rastrigin())

if __name__ == '__main__':
    main()