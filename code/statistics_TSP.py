import csv
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

import helpers
import benchmark

import benchmark_functions as benchmarks



def stats():
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    global_opts = {1: 4.284176593732411, 2:6.818737637924563, 3:4.396640190210825}

    count = 0 
    functions = []
    for bench in n_dim_fun:
        statistics = pd.DataFrame()
        res = helpers.get_statistics((1,10), (1,40), global_opts[1], 1)
        statistics = statistics.append(res)
        statistics['d'] = statistics.index
        print(statistics)
        if bench.__name__ in ['ackley', 'griewank']:
            ax = statistics.plot(ax=ax, kind='line', y='Mean', rasterized=True, logy=True, c=colors[count], xticks=[2,5,10,20, 50, 100])
            ax = statistics.plot(ax=ax, kind='line', x='d', rasterized=True, logy=True, y='Std Dev', c=colors[count], linestyle=':', xticks=[2,5,10,20, 50, 100])
            # ax = plt.errorbar(y=statistics['Mean'], x=statistics['d'], yerr=statistics['Std Dev'])
            count += 1
            ax.get_legend().remove()
            functions.append(statistics['Function'][2])
    legenda = zip(colors, functions)
    patches = []
    for combi in legenda:
        patches.append(mpatches.Patch(color=combi[0], label=combi[1]))
    # plt.yscale('log')
    plt.legend(handles=patches)
    plt.xlabel('Dimension')
    plt.show()

def plot_stats():
    stats()


def main():
   plot_stats()

if __name__ == '__main__':
    main()