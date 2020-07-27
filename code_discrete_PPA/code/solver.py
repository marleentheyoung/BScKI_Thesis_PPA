from helpers import read_tsp, normalize, transform_solution
from distance import select_closest, euclidean_distance, route_distance
from route import Route

import math
import random
import pandas as pd

def strip(problem, env):
    """Solves the TSP through the use of the strip algorithm.
 
    :param problem (TSP object): problem instance object
    :return: ? route ?
    """
    # Obtain the normalized set of cities (w/ coord in [0,1])
    cities, n = problem
    cities[['x', 'y']] = normalize(cities[['x', 'y']])

    # Determine strip width
    r = math.sqrt(n/2)
    strip_width = 1/r

    # Generate tuples that indicate the strip boundaries
    boundaries = [strip_width*i for i in range(0,math.floor(r) + 2)]
    intervals = zip(boundaries, boundaries[1:])

    route = pd.DataFrame()
    for index, strip in enumerate(intervals):
        strip_df = cities[(cities['x'] >= strip[0]) & (cities['x'] < strip[1])]
        if (index % 2) == 0:
            strip_df = strip_df.sort_values(by=['y'])
        else:
            strip_df = strip_df.sort_values(by=['y'], ascending=False)
        route = route.append(strip_df)
    route = route.set_index([pd.Index([i for i in range(len(route))])])
    route = route.append(route.loc[[0]])
    route_df = route.set_index([pd.Index([i for i in range(len(route))])])
    return Route(route_df, env)

def greedy(problem, env):
    # Obtain the normalized set of cities (w/ coord in [0,1])
    cities, n = problem
    cities[['x', 'y']] = normalize(cities[['x', 'y']])
    solution = pd.DataFrame()

    # Pick random start city
    start_index = random.randrange(0, len(cities))
    start = cities.loc[start_index]
    cities = cities.drop([start_index])

    while len(cities) > 0:
        next_city = select_closest(cities[['x', 'y']], start[['x', 'y']])
        solution = solution.append(cities.loc[next_city])
        cities = cities.drop([next_city]).reset_index(drop=True)    
    return Route(solution, env)


def random_solver(problem, env):
    """ DOCSTRING """
    # Obtain the normalized set of cities (w/ coord in [0,1])
    cities, n = problem
    cities[['x', 'y']] = normalize(cities[['x', 'y']])
    
    # Generate a random permutation of the cities
    route = cities.sample(frac=1).reset_index(drop=True)
    return Route(route, env)
