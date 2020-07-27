""" 
Author of this code: W. Vrielink

Further documentation:
https://github.com/WouterVrielink/FWAPPA
"""

import math
import numpy as np
# from point import Point
from solver import strip, random_solver, greedy
from route import Route
from distance import select_closest, euclidean_distance, route_distance



class Environment(object):
    """
    The Environment class interfaces with the Point class in such a way that the
    algorithm class does not have to know anything about the benchmark function
    or its properties.
    """

    def __init__(self, problem, m):
        """
        args:
            bounds: the boundaries of the bench
            bench: the benchmark function object
        """
        self.problem = problem
        self.m = m

        # Prepare data lists for statistics
        self.evaluation_statistics = []
        self.evaluation_statistics_best = []
        self.generation_statistics = []

        self.generation_number = 0
        self.evaluation_number = 0
        self.cur_best = math.inf
        self.cur_best_route = None

    def get_random_population(self):
        """
        Randomly initializes a population of size N.

        args:
            N (int): the number of individuals to create

        returns:
            A list of Point objects.
        """
        print("-------- CREATING START POPULATION --------")
        # return [strip(self.problem, self)] + [random_solver(self.problem, self) for _ in range(rand)] + [greedy(self.problem, self) for _ in range(greed)]
        return [random_solver(self.problem, self) for _ in range(self.m)]


    def calculate_fitness(self, route_df):
        """
        Calculate the fitness of an individual that is at a specific position.

        args:
            pos: a set of coordinates

        returns:
            The value of the bench on that position (float).
        """
        self.evaluation_number += 1
        fitness = route_distance(route_df)
        self.evaluation_statistics.append(fitness)

        # Update curbest value
        if fitness < self.cur_best:
            self.cur_best = fitness
            self.cur_best_route = Route(route_df, self)

        self.evaluation_statistics_best.append(self.cur_best)
        self.generation_statistics.append(self.generation_number)
        return fitness

    def get_evaluation_statistics(self):
        return list(range(1, self.evaluation_number + 1)), self.evaluation_statistics

    def get_evaluation_statistics_best(self):
        return list(range(1, self.evaluation_number + 1)), self.evaluation_statistics_best

    def get_generation_statistics(self):
        return list(range(1, self.evaluation_number + 1)), self.generation_statistics
