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
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import benchmark

import benchmark_functions as benchmarks

if __name__ == "__main__":
    bench_fun = [getattr(benchmarks, fun) for fun in dir(benchmarks) if hasattr(getattr(benchmarks, fun), 'is_n_dimensional')]
    n_dim_fun = [fun for fun in bench_fun if fun.is_n_dimensional]

    for fun in n_dim_fun:
        function = fun.__name__
        plot_df = pd.DataFrame()
        i=0
        fig, ax = plt.subplots()

        for dim in [2, 5, 10, 20, 50, 100]:
            df1 = pd.read_csv(f'../sample/PlantPropagation_n_max=1_m=10000/{function}/{dim}d/1_10000_2.csv')
            mean=df1['value'].mean()
            # sns.distplot(df1['value'].tolist(), ax=ax)
            # ax.axvline(mean, color='r', linestyle='--')

            df2 = pd.read_csv(f'../lisa_data/cross/median_best/relation_n_max_to_m_{function}{dim}d.csv')
            mini=df2['median_best'].min()
            maxi=df2['median_best'].max()
            print(function, dim)
            rel_min = mini/mean
            rel_max = maxi/mean
            par_dependency = maxi/(mean - maxi) - mini/(mean - maxi)
            plot_df = plot_df.append(pd.DataFrame({'dimension':dim, 'rel_min':rel_min, 'rel_max':rel_max, 'rel_max-rel_min':par_dependency}, index=[i]))
            i+=1
        print(plot_df['dimension'].tolist())
        ax.plot(plot_df['dimension'].tolist(), plot_df['rel_max-rel_min'].tolist())
        plt.xticks([2,5,10,20,50,100])
        plt.title(function.capitalize())
        plt.xlabel('Dimension')
        plt.ylabel('Parameter dependency')
        # sns.distplot(df2['median_best'].tolist(), ax=ax)
        # ax.axvline(maxi, color='b', linestyle='--')
        # ax.axvline(mini, color='g', linestyle='--')
        # plt.xlim(-100,28000)
        plt.show()
        print("yes")
        
   