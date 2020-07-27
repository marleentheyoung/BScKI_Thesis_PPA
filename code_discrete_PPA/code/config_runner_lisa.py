import csv
import pandas as pd
import statistics as stats
from decimal import Decimal
import os
import sys

def write_to_csv(data, output_dir):
    filename = f"{output_dir}/relation_n_max_to_m_TSP_problem_3.csv"
    with open(filename, 'w') as cross_csv:
        fieldnames = ['n_max', 'm', 'median_best']
        data_writer = csv.DictWriter(cross_csv, fieldnames=fieldnames)
        data_writer.writeheader()

        for item in data:
            data_writer.writerow(item)

def get_median_best(input_dir, output_dir):
    data = []
    for n_max in range(1, 11):
        for m in range(1, 41):
            optimas = []
            for it in range(1,6):
                filename = f"{input_dir}/PPA_m={m}_n_max={n_max}/{it}_problem3.csv"
                print(filename)
                with open(filename, newline='') as csvfile:
                    df = pd.read_csv(filename)
                    optimum = ((df.iloc[-1:])['curbest']).values[0]
                    optimas.append(optimum)
            med = stats.median(optimas)
            data.append({'n_max':n_max, 'm':m, 'median_best':med})
    write_to_csv(data, output_dir)
    return

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Please specify the output folder. \nUsage: python3 batchrunner_lisa.py [input_dir] [output_dir]")
        quit()

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    get_median_best(input_dir, output_dir)