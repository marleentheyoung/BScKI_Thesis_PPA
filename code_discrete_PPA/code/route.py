from distance import select_closest, euclidean_distance, route_distance
from random import randrange

import matplotlib.pyplot as plt
import pandas as pd

class Route():
    def __init__(self, route_df, env):
        self.route_df = route_df
        self.env = env
        self._fitness = None

    @property
    def fitness(self):
        """
        Calculates the fitness of the individual if it was not already
        calculated.

        returns:
            The fitness of an individual
        """
        if self._fitness is None:
            self._fitness = self.env.calculate_fitness(self.route_df)
        return self._fitness
    
    def get_short_runner(self):
        """ 2-opt rule """
        index = randrange(len(self.route_df) - 1)
        runner = self.route_df.copy()

        # Apply 2-opt rule on the route
        runner = self.two_opt(runner)
        return Route(runner, self.env)

    def get_long_runner(self):
        runner = self.route_df.copy(deep=True)

        # Apply sequence of three 2-opt rules
        for _ in range(3):
            runner = self.two_opt(runner)
        return Route(runner, self.env)

    def get_custom_runner(self, n_runners, n_swaps):
        route = self.route_df.copy(deep=True)
        for runner in range(n_runners):
            for swap in range(n_swaps):
                route = self.two_opt(route)
        return Route(route, self.env)

       
    def two_opt(self, route_df):
        index = randrange(len(route_df) - 1)

        swap1, swap2 = route_df.iloc[index].copy(), route_df.iloc[index+1].copy()
        route_df.iloc[index], route_df.iloc[index+1] = swap2, swap1
        return route_df
    
    def plot_route(self):
        """ Plots found route """
        ax = self.route_df.plot.scatter(
                x='x',
                y='y',
                c='DarkBlue'
            )

        for index, row in self.route_df.iterrows():
            if index != len(self.route_df) - 1:
                vertice = self.route_df.loc[[index, index+1]]
                plt.plot(vertice['x'].tolist(), vertice['y'].tolist(), 'ro', linestyle=':', marker='o', markersize=4)
        plt.show()