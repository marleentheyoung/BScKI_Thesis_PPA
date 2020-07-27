"""
This file contains the Heatmap class. Running this file will generate heatmaps
for five benchmark test functions.
"""

import seaborn as sns
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math

class Heatmap:
    def __init__(self, fontsize, fsize=(10,40), cbar=False, lowerbound=None, upperbound=None, xticklabels=True, yticklabels=True):
        """
        Vizualizes a heatmap for a given function and specified statistic measure.

        args:
            function: the boundaries of the bench
            mode: a list of the global minima in the function
            global_optimum: global optimum corresponding to the benchmark
            mode: statistic measure
            fontsize: fontsize of axis labels
            fsize: size of output figure
            cbar: boolean that sets color bar if True
            lowerbound: lowerbound of the color bar ticks
            upperbound: upperbound of the color bar ticks
        """
        self.fontsize = fontsize
        self.fsize = fsize
        self.cbar = cbar
        self.lowerbound = lowerbound
        self.upperbound = upperbound
        self.xticklabels = xticklabels
        self.yticklabels = yticklabels

    def create_ticks(self):
        """
        Creates labels for both axes. 
        """
        # Set x axis labels
        if self.xticklabels:
            xticks = ['']
            for i in range(2,11, 2):
                xticks.append(i)
                if i != 10:
                    xticks.append('')
        else:
            xticks=False
        
        # Set y axis labels
        if self.yticklabels:
            yticks = ['','','','']
            for i in range(5,41, 5):
                yticks.append(i)
                if i != 40:
                    for j in range(4):
                        yticks.append('')
        else:
            yticks=False
        return (xticks, yticks)    
    
    def get_lowerbound(self, data):
        """
        Returns lowerbound of the ticks on cbar.
        """
        if self.lowerbound:
            print("if: ")
            mini = self.lowerbound
        else:
            print("else: ")
            mini = data.min().min()
            print(mini)
        return mini
    
    def get_upperbound(self, data):
        """
        Returns upperbound of the ticks on cbar.
        """
        if self.lowerbound:
            mini = self.upperbound
        else:
            mini = data.max().max()
        return mini

    def visualize(self):
        """
        Creates heatmap visualization for specified function and statistic mode.
        """
        sns.set(font_scale=4.5)
        filename = f"data/cross/relation_n_max_to_m_TSP_problem_3.csv"
        results = pd.read_csv(filename)

        # Subtract the global optimum to make all functions converge to 0
        global_opts = {1: 4.284176593732411, 2:6.818737637924563, 3:4.396640190210825}
        results['median_best'] = results['median_best'].subtract(global_opts[3])
        data = results.pivot('m', 'n_max', 'median_best')
        print(data)
        fig, ax = plt.subplots(figsize=self.fsize)
       
        mini = self.get_lowerbound(data)
        maxi = self.get_upperbound(data)        
        print("mini: ", mini)
        print("maxi: ", maxi)
        log_norm = LogNorm(vmin=data.min().min(), vmax=1)
        cbar_ticks = [math.pow(10, i) for i in range(math.floor(math.log10(mini)), 1+math.ceil(math.log10(maxi)))]
        xticks, yticks = self.create_ticks()
        print(xticks, yticks)
        display = sns.heatmap(
            data,
            norm=log_norm,
            cbar=self.cbar,
            cbar_kws={"ticks": cbar_ticks},
            annot=False,
            vmax=maxi,
            vmin=mini,
            cmap='YlGnBu',
            ax=ax,
            yticklabels=yticks,
            xticklabels=xticks
        )

        display.invert_yaxis()
        ax.tick_params(labelsize=self.fontsize)
        ax.set_ylabel('')    
        ax.set_xlabel('')

        # Save to PNG file
        fig = display.get_figure()
        fig_name = f"data/heatmap_TSP_problem_3_normalized_sameaxis_log.png"
        fig.savefig(fig_name, bbox_inches='tight')


if __name__ == "__main__":
    result = Heatmap(55, cbar=True, fsize=(12, 40), lowerbound=6.052351128239311, upperbound=12.405237851793686)
    result.visualize()
