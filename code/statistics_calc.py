import csv
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

import helpers
import benchmark

import benchmark_functions as benchmarks

def stats():
    bench_fun = [getattr(benchmarks, fun) for fun in dir(benchmarks) if hasattr(getattr(benchmarks, fun), 'is_n_dimensional')]
    n_dim_fun = [fun for fun in bench_fun if fun.is_n_dimensional]

    fig, ax = plt.subplots()

    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    count = 0 
    functions = []
    df = pd.DataFrame()
    for bench in n_dim_fun:
        statistics = pd.DataFrame()
        for d in [2,5,10,20, 50, 100]:
            bench.dims = d
            res = helpers.get_statistics((1,10), (1,40), bench.__name__, bench.global_minima[0][0], d)
            statistics = statistics.append(res)
        print(statistics)
        df = df.append(statistics)
    print(df)
    df.to_csv('data/stats_nd2.csv')
        # print(type(statistics))
        # quit()
    #     statistics['d'] = statistics.index
    #     print(statistics)
    #     if bench.__name__ in ['ackley', 'griewank']:
    #         ax = statistics.plot(ax=ax, kind='line', y='Mean', rasterized=True, logy=True, c=colors[count], xticks=[2,5,10,20, 50, 100])
    #         ax = statistics.plot(ax=ax, kind='line', x='d', rasterized=True, logy=True, y='Std Dev', c=colors[count], linestyle=':', xticks=[2,5,10,20, 50, 100])
    #         # ax = plt.errorbar(y=statistics['Mean'], x=statistics['d'], yerr=statistics['Std Dev'])
    #         count += 1
    #         ax.get_legend().remove()
    #         functions.append(statistics['Function'][2])
    # legenda = zip(colors, functions)
    # patches = []
    # for combi in legenda:
    #     patches.append(mpatches.Patch(color=combi[0], label=combi[1]))
    # # plt.yscale('log')
    # plt.legend(handles=patches)
    # plt.xlabel('Dimension')
    # plt.show()

def plot_stats():
    stats()


def main():
   plot_stats()

if __name__ == '__main__':
    main()