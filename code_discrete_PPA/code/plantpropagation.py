
import math
import random
import numpy as np

from environment import Environment
# from point import Point


class PPA1(object):
    """
    Python replication of the Plant Propagation algorithm as described in http://repository.essex.ac.uk/9974/1/paper.pdf
    """

    def __init__(self, problem, max_generations, m, y=0.5):
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

        self.m = m
        self.y = y #????

    def get_runners(self):
        """
        Create all the children for this plant.

        returns:
            A list of Point objects (children).
        """
        runners = []

        # Take top 10% of population
        top = self.population[:int(self.m/10)]
        bottom = self.population[int(self.m/10):]

        # Create short runners for top 10%
        for i in range(1, len(top)+1):
            # Determine number of runners to create
            n = math.floor(10/i)
            for _ in range(n):
                runner = top[i-1].get_short_runner()
                if runner.fitness < top[i-1].fitness:
                    runners.append(runner)
                    
        # Create long runners for the rest
        for route in bottom:
            runner = route.get_long_runner()
            if runner.fitness < route.fitness:
                runners.append(runner)  
        return runners

    def start(self, ret=False):
        """
        Starts the algorithm. Performs generations until the max number of
        evaluations is passed.

        Note that the algorithm always finishes a generation and can therefore
        complete more evaluations than defined.
        """
        print("Starting algorithm ...\n")
        while self.env.generation_number <= self.max_generations:
            # Sort and select population
            self.population = sorted(self.population, key=lambda plant: plant.fitness)[:self.m]

            # Create offspring
            self.population += self.get_runners()

            self.iteration += 1
            self.env.generation_number += 1    

        return self.env.cur_best_route
            
class PPA2(object):
    """
    Python replication of the Plant Propagation algorithm as described in http://repository.essex.ac.uk/9974/1/paper.pdf
    """

    def __init__(self, problem, max_evaluations, m, n_max, s_max, y=0.5):
        """
        args:
            bench: the benchmark function object
            bounds: the boundaries of the bench
            max_evaluations (int): the maximum number of evaluations to run
            m (int): the population size
            max_runners (int): the maximum number of runners per individual
        """
        self.problem = problem
        self.m = m
        self.env = Environment(self.problem, self.m)

        self.population = self.env.get_random_population()

        self.iteration = 0
        self.max_evaluations = max_evaluations
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
            if self.x_max == self.x_min:
                N_i = 0.5
            else:
                N_i = 0.5 * (math.tanh(4 * ((self.x_max - route.fitness) / (self.x_max - self.x_min)) - 2) + 1)
            n_runners = math.ceil(self.n_max * N_i * (random.random()))
            n_swaps = math.ceil(self.s_max * (random.random()) * (1 - N_i))
   
            runner = route.get_custom_runner(n_runners, n_swaps)
            runners.append(runner)
        return runners
    
    @property
    def x_max(self):
        """ Returns element with the highest objective value in the Population """
        self._xmax = sorted(self.population, key=lambda plant: plant.fitness)[:self.m][-1].fitness
        return self._xmax

    @property
    def x_min(self):
        """ Returns element with the lowest objective value in the Population """
        self._xmin = sorted(self.population, key=lambda plant: plant.fitness)[0].fitness
        return self._xmin

    def start(self, ret=False):
        """
        Starts the algorithm. Performs generations until the max number of
        evaluations is passed.

        Note that the algorithm always finishes a generation and can therefore
        complete more evaluations than defined.
        """
        print("Starting algorithm ...\n")
        while self.env.evaluation_number <= self.max_evaluations:
            # Sort and select population
            self.population = sorted(self.population, key=lambda plant: plant.fitness)[:self.m]

            # Create offspring
            self.population += self.get_runners()

            self.iteration += 1
            self.env.generation_number += 1    

        return self.env.cur_best_route