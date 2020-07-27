import csv
import os
import sys

import pandas as pd

def main():
    time = 0
    for function in ['ackley', 'cigar', 'elipse', 'griewank', 'rastrigin', 'rosenbrock', 'schwefel', 'sphere', 'tablet']:
        for n_max in range(10, 11):
            for m in range(1, 41):
                for d in [2,5,10,20,50,100]:
                    filename = f"../scratch/lisa_data/PlantPropagation_n_max={n_max}_m={m}/{function}/{d}d/time.csv"
                    times = pd.read_csv(filename)
                    time += times['Time'].sum()
    
    print(time, " seconds")

if __name__ == "__main__":
    main()