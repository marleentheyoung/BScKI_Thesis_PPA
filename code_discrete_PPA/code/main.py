from sys import argv
import math

import numpy as np
import pandas as pd
from timeit import default_timer as timer

import helpers
from plantpropagation import PPA1, PPA2
from helpers import read_tsp, normalize, transform_solution
from distance import select_closest, euclidean_distance, route_distance
# from plot import plot_route
from solver import strip, greedy, random
from route import Route
from environment import Environment

def do_run(problem, max_evals, m, reps, version, n_max=None, s_max=None, ret=False):
    print(f"Running m={m} and n_max={n_max} on PPA-{version}")
    for repetition in range(reps):
        filename_stats = helpers.get_name(version, repetition, m, n_max)

        if version == '1':
            PPA = PPA1(problem, max_evals, m)
        else:
            PPA = PPA2(problem, max_evals, m, n_max, s_max)

        print(f"\tRepetition {repetition} / {reps} - running")
        start = timer()
        best = PPA.start(ret=ret)
        end = timer()

        print(f"\tRepetition {repetition} / {reps} - saving")
        helpers.save_to_csv(PPA, filename_stats)


def main():
    # if len(argv) != 4:
    #     print("Correct use: python3 code/main.py problems/<filename>.tsp n_start n_end")
    #     return -1
    # n_start = int(argv[2])
    # n_end = int(argv[3])
    problem = read_tsp('problems/instance_1.tsp.txt')

    # for n_max in range(n_start, n_end):
    #     for m in range(1,41):
    #         do_run(problem, 4000, m, 5, version='2', n_max=n_max, s_max=20, ret=True)
    solution = read_tsp('solutions/instance_1.opt.tour.tsp.txt', solution=True)
    optimal_route = transform_solution(problem, solution)
    env = Environment(optimal_route, 30)
    ro = Route(optimal_route, env)
    ro.plot_route()

    # print('Route found of length {}'.format(distance))
    # print('Optimal route has length {}'.format(optimal_distance))

    # plot_route(route)
    # plot_route(optimal_route)



if __name__ == '__main__':
    main()