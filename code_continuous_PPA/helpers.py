"""
This file contains the code needed to generate a variety of parameter configurations. Next to this,
the functions get_min_min() and get_max_min() are necessary for the heatmap visualizations.

"""

import pandas as pd
import statistics as stats

MODES = ['average_best', 'median_best', 'min_min', 'optimum']

def config_generator(n_range=[1,11], m_range=[1, 41]):
    """
    Generates a variety of parameter configurations for parameters
    popSize and max_runners

    args:
        n_range: range of n_max
        m_range: range of m (popSize)

    returns:
        A list of configuration dicts
    """
    configs = []
    config = {}

    for n_max in range(n_range[0], n_range[1]):
        for m in range(m_range[0], m_range[1]):
            config["m"] = m
            config["max_runners"] = n_max
            configs.append({f"n_max={n_max}_m={m}":config})
    return configs

def get_max_min(function):
    """
    Returns the highest (worst) found median optimum over all 
    runs of all tested functions.

    args:
        n_range: range of n_max
        m_range: range of m (popSize)

    returns:
        max min 
    """
    max_mins = []
    for d in [2,5,10,20,50,100]:
        filename = f"lisa_data/cross/median_best/relation_n_max_to_m_{function.__name__}{d}d.csv"
        results = pd.read_csv(filename)
        max_min = results['median_best'].max() - function.correction
        max_mins.append(max_min)
    return max(max_mins)

def get_min_min(function):
    """
    Returns the best found (min min) median optimum over all 
    runs of all test functions.

    args:
        n_range: range of n_max
        m_range: range of m (popSize)

    returns:
        min min (float)
    """
    min_mins = []
    for d in [2,5,10,20,50,100]:
        filename = f"lisa_data/cross/median_best/relation_n_max_to_m_{function.__name__}{d}d.csv"
        results = pd.read_csv(filename)
        min_min = results['median_best'].min() - function.correction
        min_mins.append(min_min)
    return min(min_mins)

def get_statistics(n_range, m_range, function, optimum, d):
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

    filename = f"lisa_data/cross/median_best/relation_n_max_to_m_{function}{d}d.csv"
    results = pd.read_csv(filename)
    results = results[(results['n_max'] >= n_range[0]) & (results['n_max'] <= n_range[1])]
    results = results[(results['m'] >= m_range[0]) & (results['m'] <= m_range[1])]

    stddevs = []
    means = []
    for it in range(1, 11):
        filename2 = f"sample/PlantPropagation_n_max=1_m=10000/{function}/{d}d/{it}_10000_2.csv"
        results2 = pd.read_csv(filename2)
        stddevs.append(results2['curbest'].std())
        means.append(results2['curbest'].mean())

    return pd.DataFrame({'Function':function, 'Mean':results['median_best'].mean(), 'Std Dev':results['median_best'].std(), \
                        'Mean Sample': stats.median(means), 'Std Dev Sample':stats.median(stddevs)}, index=[d])