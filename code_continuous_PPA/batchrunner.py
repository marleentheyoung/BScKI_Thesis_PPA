"""
-- Author of this code: W. Vrielink --
https://github.com/WouterVrielink/FWAPPA

This file holds all the code required to run all experiments with the
parameter configurations that are specified in CONFIGS_DICT.
"""

import json
import os

import numpy as np
from timeit import default_timer as timer

import helper_tools
from helpers import config_generator

# Adjust range of parameter values to test here
CONFIGS_DICT = config_generator(n_range=[1,2], m_range=[1,2])

def load_config(file):
    """
    Loads a config file (JSON) into a dictionary.

    args:
        file (str): the file that should be loaded

    returns:
        A config dictionary.
    """
    with open(file, 'r') as f:
        config = json.load(f)
    return config

def do_run(alg, bench, max_evaluations, config, reps, bounds=None, dims=2, prefix=None, verbose=True, version="DEFAULT"):
    """
    Performs a run with the given parameters. Automatically saves the results in
    the proper folders.

    args:
        alg: the algorithm object
        bench: the benchmark function object
        max_evaluations (int): the maximum amount of evaluations to run
        reps (int): the amount of times an experiment should be repeated
        bounds: a tuple containing the bounds to set for the bench
        dims (int): the amount of dimensions in the bench
        prefix (str): an optional prefix for the experiment name
        version (str): the name of the parameter-set
        verbose (bool): whether the function should be verbose
    """
    if not bounds:
        bounds = bench.bounds

    if verbose:
        print("--------------------------------------")
        print(f"Running {alg.__name__} on {bench.__name__} in {dims}D... for {max_evaluations} evaluations")

    filename_time = helper_tools.get_time_name(alg, bench, version, dims, 'hillclimber', prefix)

    for repetition in range(1, reps + 1):
        filename_stats = helper_tools.get_name(alg, bench, max_evaluations, version, dims, repetition, 'hillclimber', prefix)

        if os.path.isfile(filename_stats):
            print(f"\tRepetition {repetition} / {reps} - exists") if verbose else _
            continue

        alg_instance = alg(bench, bounds, max_evaluations, **config)

        print(f"\tRepetition {repetition} / {reps} - running") if verbose else _
        start = timer()
        alg_instance.start()
        end = timer()
        print(filename_stats)
        print(f"\tRepetition {repetition} / {reps} - saving") if verbose else _
        helper_tools.save_to_csv(alg_instance, filename_stats)
        # helper_tools.save_time(end - start, alg_instance.env.evaluation_number, repetition, filename_time)


if __name__ == "__main__":
    import benchmark
    import benchmark_functions as benchmarks

    from plantpropagation import PlantPropagation

    # evaluations = 10000
    repetitions = 10
    maxDims = 100
    evaluations = 10000

    # Prepare globals
    bench_fun = [getattr(benchmarks, fun) for fun in dir(benchmarks) if hasattr(getattr(benchmarks, fun), 'is_n_dimensional')]
    two_dim_fun = [fun for fun in bench_fun if not fun.is_n_dimensional]
    n_dim_fun = [fun for fun in bench_fun if fun.is_n_dimensional]

    non_center_two_dim_fun = [fun for fun in two_dim_fun if (0, 0) not in fun.global_minima]
    non_center_n_dim_fun = [fun for fun in n_dim_fun if (0) not in fun._global_minima]

    algorithms = [PlantPropagation]
    n_max_params = [str(x) for x in range(2,11)]

    # 2-dimensional
    for alg in algorithms:
        for config in CONFIGS_DICT:
            for bench in two_dim_fun:
                for config_name in config:
                    print(config_name)
                    do_run(alg, bench, evaluations, config[config_name], repetitions, version=config_name)

    # # N-dimensional
    # for alg in algorithms:
    #     for config in CONFIGS_DICT:
    #         for dims in [2,5,10,20,50,100]:
    #             for bench in n_dim_fun:
    #                 for config_name in config:
    #                     print(config_name)
    #                     bench.dims = dims

    #                     do_run(alg, bench, evaluations, config[config_name], repetitions, dims=dims, version=config_name)

    #                     bench_add = benchmark.apply_add(bench)

    #                     do_run(alg, bench, evaluations, config[config_name], repetitions, dims=dims, version=config_name)
               
                # print("tweeede loooop")
                # for bench in non_center_n_dim_fun:
                #     for config_name in config:
                #         bench.dims = dims

                #         bench_center = benchmark.apply_add(bench, value=bench.global_minima[0], name='_center')

                #         do_run(alg, bench_center, evaluations, config[config_name], repetitions, dims=dims, version=config_name)