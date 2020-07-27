
import math
import random
import numpy as np

from environment import Environment
from route import Route
# from point import Point


class PPA2(object):
    """
    Python replication of the Plant Propagation algorithm as described in http://repository.essex.ac.uk/9974/1/paper.pdf
    """

    def __init__(self, problem, max_generations, m, n_max, s_max, y=0.5):
        """
        args:
            bench: the benchmark function object
            bounds: the boundaries of the bench
            max_evaluations (int): the maximum number of evaluations to run
            m (int): the population size
            max_runners (int): the maximum number of runners per individual
        """
        self.problem = problem
        self.env = Environment(self.problem)

        self.population = self.env.get_random_population(rand=(m-1))

        self.iteration = 0
        self.max_generations = max_generations
        self.n_max = n_max
        self.s_max = s_max

        self.m = m
        self.y = y #????

        self._xmax = None
        self._xmin = None

    def get_runners(self):
        """
        Create all the children for this plant.

        returns:
            A list of Point objects (children).
        """
        runners = []

        # Create short runners for top 10%
        for route in self.population:
            N_i = 0.5 * (math.tanh(4 * ((route.x_max - route.fitness) / (route.xmax - route.xmin)) - 2) + 1)
            n_runners = self.n_max * N_i * (random.random() - 0.5)
            n_swaps = self.s_max * (random.random() - 0.5) * (1 - N_i)
            runner = route.get_custom_runner(n_runners, n_swaps)
        return runners
    
    @property
    def x_max(self):
        """ Returns element with the highest objective value in the Population """
        self._xmax = sorted(self.population, key=lambda plant: plant.fitness)[0]
        return self._xmax

    @property
    def x_min(self):
        """ Returns element with the lowest objective value in the Population """
        self._xmin = sorted(self.population, key=lambda plant: plant.fitness)[-1]
        return self._xmin

    def start(self, ret=False):
        """
        Starts the algorithm. Performs generations until the max number of
        evaluations is passed.

        Note that the algorithm always finishes a generation and can therefore
        complete more evaluations than defined.
        """
        print("Starting algorithm ...\n")
        while self.env.generation_number <= self.max_generations:
            print("Generation:", self.env.generation_number + 1)

            # Sort and select population
            self.population = sorted(self.population, key=lambda plant: plant.fitness)[:self.m]
            print("Population selected ...")

            # Create offspring
            self.population += self.get_runners()
            print("Offspring generated ... \n")

            self.iteration += 1
            self.env.generation_number += 1    

        return self.population
            