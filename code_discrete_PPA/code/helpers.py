import csv
import os
import pandas as pd
import numpy as np


def read_tsp(filename, solution=False):
    """
    Read a file in .tsp format into a pandas DataFrame
    The .tsp files can be found in the TSPLIB project. Currently, the library
    only considers the possibility of a 2D map.
    """
    if solution:
        start = 'TOUR_SECTION'
        start2 = ''
    else:
        start = 'NODE_COORD_SECTION'
        start2 = 'EDGE_WEIGHT_SECTION'

    with open(filename) as f:
        node_coord_start = None
        dimension = None
        lines = f.readlines()
        print(lines)
        # Obtain the information about the .tsp
        i = 0
        while not dimension or not node_coord_start:
            line = lines[i]
            if line.startswith('DIMENSION:') or line.startswith('DIMENSION :'):
                dimension = int(line.split()[-1])
            if line.startswith(start) or line.startswith(start2):
                node_coord_start = i
            i = i+1

        print(f"Problem instance with {dimension} cities read.")

        f.seek(0)

        # Read a data frame out of the file descriptor
        cities = pd.read_csv(
            f,
            skiprows=node_coord_start + 1,
            sep=' ',
            names=['city', 'x', 'y'],
            dtype={'city': str, 'x': np.float64, 'y': np.float64},
            header=None,
            nrows=dimension
        )
        # cities.set_index('city', inplace=True)
        return (cities, dimension)

def normalize(points):
    """
    Return the normalized version of a given vector of points.
    For a given array of n-dimensions, normalize each dimension by removing the
    initial offset and normalizing the points in a proportional interval: [0,1]
    on y, maintining the original ratio on x.
    """
    ratio = (points.x.max() - points.x.min()) / (points.y.max() - points.y.min()), 1
    ratio = np.array(ratio) / max(ratio)
    norm = points.apply(lambda c: (c - c.min()) / (c.max() - c.min()))
    return norm.apply(lambda p: ratio * p, axis=1)

def transform_solution(problem, route):
    print(problem)
    problem_df = problem[0]
    route_df = route[0]
    transformed_df = pd.DataFrame()

    # Merge city coordinates and  
    for index, row in route_df.iterrows():
        xy = problem_df[(problem_df['city'] == row['city'])]
        transformed_df = transformed_df.append(xy)
    # Re-Index
    transformed_df = transformed_df.set_index([pd.Index([i for i in range(len(transformed_df))])])
    transformed_df = transformed_df.append(transformed_df.loc[[0]])
    transformed_df = transformed_df.set_index([pd.Index([i for i in range(len(transformed_df))])])

    # transformed_df[['x', 'y']] = normalize(transformed_df[['x', 'y']])
    
    # Return tuple with Solution Dataframe and dimension
    return transformed_df


def build_path(version, m, n_max):
    """
    Builds a path string with given parameters.

    args:
        alg: the algorithm object
        bench: the benchmark function object
        version (str): the name of the parameter-set
        dims (int): the amount of dimensions used in the test
        prefix (str): reserved for unusual tests that require a different dir

    returns:
        A path string.
    """
    return f'data/PlantPropagation{version}_TSP/PPA_m={m}_n_max={n_max}/'


def get_name(version, rep, m, n_max):
    """
    Builds the entire path string for the csv data files.

    args:
        alg: the algorithm object
        bench: the benchmark function object
        version (str): the name of the parameter-set
        dims (int): the amount of dimensions used in the test
        rep (int): the "how many-th" time this bench was run
        prefix (str): reserved for unusual tests that require a different dir

    returns:
        A path string with a #.csv filename.
    """
    return f'{build_path(version, m, n_max)}/{str(rep+1)}_problem3.csv'


def get_time_name(alg, bench, version, dims, output_dir, prefix=None):
    """
    Builds the entire path string for the time data files.

    args:
        alg: the algorithm object
        bench: the benchmark function object
        version (str): the name of the parameter-set
        dims (int): the amount of dimensions used in the test
        prefix (str): reserved for unusual tests that require a different dir

    returns:
        A path string with time.csv.
    """
    return f'{build_path(alg, bench, version, dims, output_dir, prefix)}/time.csv'

def save_to_csv(alg, filename):
    """
    Saves the evaluation value, current best, and the generation number to the
    given filename. Extracts the data directly from the object instance.

    args:
        alg: algorithm object instance
        filename (str): the complete filepath + filename of the target
    """
    x, y = alg.env.get_evaluation_statistics()
    _, best_y = alg.env.get_evaluation_statistics_best()
    _, generations = alg.env.get_generation_statistics()

    check_folder(filename)

    with open(filename, mode='w') as file:
        writer = csv.writer(file)

        writer.writerow(['evaluation', 'value', 'curbest', 'generation'])

        for row in zip(x, y, best_y, generations):
            writer.writerow(row)

def check_folder(filepath):
    """
    Checks if a filepath exists, otherwise creates the directory.

    args:
        filepath (str): the filepath to be checked
    """

    dirname = os.path.dirname(filepath)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

def save_time(time, total_evals, rep, filename):
    """
    Saves the time taken, the total number of evaluations and the repetition
    number to the given filename.

    args:
        time (float): time taken in seconds
        total_evals (int): the total number of evaluations that was performed in
                this time
        rep (int): the "how many-th" time this bench was run
        filename (str): the complete filepath + filename of the target
    """
    # Check if filepath is accessible
    check_folder(filename)

    # Append to end ('a')
    with open(filename, mode='a') as file:
        writer = csv.writer(file)

        if rep == 1:
            writer.writerow(['Time', 'Total_Evaluations'])

        writer.writerow([time, total_evals])

def get_statistics(n_range, m_range, optimum, problem_number):
    """
    Calculates mean and sigma of values within a range of parameter 
    configurations.

    args:
        n_range: range of n_max
        m_range: range of m (popSize)
        function: name of function
        optimum: global optimum of specified function

    returns:
        tuple (mean, sigma)
    """
    res = {}

    filename = f"data/cross/relation_n_max_to_m_TSP_problem_{problem_number}.csv"
    results = pd.read_csv(filename)
    results['median_best'] = results['median_best'].subtract(optimum)
    results = results[(results['n_max'] >= n_range[0]) & (results['n_max'] <= n_range[1])]
    results = results[(results['m'] >= m_range[0]) & (results['m'] <= m_range[1])]
    return pd.DataFrame({'Problem':problem_number, 'Mean':results['median_best'].mean(), 'Std Dev':results['median_best'].std()}, index=[problem_number])
