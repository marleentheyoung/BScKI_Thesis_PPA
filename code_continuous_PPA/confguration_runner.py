import csv
import pandas as pd
import statistics as stats
from decimal import Decimal

def compute_integrals():
    for function in ['branin', 'easom', 'goldstein_price', 'martin_gaddy', 'six_hump_camel']:
        data = []
        for n_max in range(2, 10):
            for m in range(20, 40):
                filename = f"../data/scores varying n_max + m/PlantPropagation_n_max={n_max}_m={m}/{function}/2d/1.csv"
                print(filename)
                with open(filename, newline='') as csvfile:
                    df = pd.read_csv(filename)
                    integral = df['curbest'].sum()
                    data.append({'n_max':n_max, 'm':m, 'integral':integral})
        write_to_csv(data, function, 'integral')
    return

def get_best():
    for function in ['branin', 'easom', 'goldstein_price', 'martin_gaddy', 'six_hump_camel']:
        data = []
        for n_max in range(1, 10):
            for m in range(5, 40):
                filename = f"../data/scores varying n_max + m/PlantPropagation_n_max={n_max}_m={m}/{function}/2d/1.csv"
                print(filename)
                with open(filename, newline='') as csvfile:
                    df = pd.read_csv(filename)
                    optimum = ((df.iloc[-1:])['curbest']).values[0]
                    data.append({'n_max':n_max, 'm':m, 'optimum':optimum})
        write_to_csv(data, function, 'optimum')
    return

def get_median_best(evals):
    for function in ['branin', 'easom', 'goldstein_price', 'martin_gaddy', 'six_hump_camel']:
        data = []
        for n_max in range(1, 11):
            for m in range(1, 41):
                optimas = []
                for it in range(1,11):
                    filename = f"../data/PlantPropagation_n_max={n_max}_m={m}/{function}/2d/{it}_{evals}.csv"
                    print(filename)
                    with open(filename, newline='') as csvfile:
                        df = pd.read_csv(filename)
                        optimum = ((df.iloc[-1:])['curbest']).values[0]
                        optimas.append(optimum)
                med = stats.median(optimas)
                data.append({'n_max':n_max, 'm':m, 'median_best':med})
        write_to_csv(data, function, 'median_best', evals)
    return

def get_min_min():
    for function in ['branin', 'easom', 'goldstein_price', 'martin_gaddy', 'six_hump_camel']:
        data = []
        for n_max in range(1, 10):
            for m in range(5, 40):
                optimas = []
                for it in range(1,11):
                    filename = f"../data/scores varying n_max + m/PlantPropagation_n_max={n_max}_m={m}/{function}/2d/{it}_{evals}_rounded.csv"
                    print(filename)
                    with open(filename, newline='') as csvfile:
                        df = pd.read_csv(filename)
                        optimum = ((df.iloc[-1:])['curbest']).values[0]
                    optimas.append(optimum)
                data.append({'n_max':n_max, 'm':m, 'min_min':min(optimas)})
        write_to_csv(data, function, 'min_min')
    return

def get_average_best():
    for function in ['branin', 'easom', 'goldstein_price', 'martin_gaddy', 'six_hump_camel']:
        data = []
        for n_max in range(1, 11):
            for m in range(1, 41):
                total = 0
                for it in range(1,11):
                    filename = f"../data/scores varying n_max + m/PlantPropagation_n_max={n_max}_m={m}/{function}/2d/{it}.csv"
                    print(filename)
                    with open(filename, newline='') as csvfile:
                        df = pd.read_csv(filename)
                        optimum = ((df.iloc[-1:])['curbest']).values[0]
                        total += optimum
                    average = total / 10
                data.append({'n_max':n_max, 'm':m, 'average_best':average})
        write_to_csv(data, function, 'average_best', '')
    return

def write_to_csv(data, function, mode, evals):
    filename = f"../data/cross/{mode}/relation_n_max_to_m_{function}_{evals}.csv"
    with open(filename, 'w') as cross_csv:
        fieldnames = ['n_max', 'm', mode]
        data_writer = csv.DictWriter(cross_csv, fieldnames=fieldnames)
        data_writer.writeheader()

        for item in data:
            data_writer.writerow(item)


get_average_best()