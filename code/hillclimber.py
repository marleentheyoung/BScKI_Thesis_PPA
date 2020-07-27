# IMPORTS
import random
import copy
import numpy as np
from numpy import median, mean
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import benchmark
import benchmark_functions as benchmarks
from plantpropagation import PlantPropagation
from batchrunner import do_run



class Hillclimber():
    def __init__(self, bench, bounds, iterations, reps=10):
        self.bench = bench
        self.bounds = bounds
        self.iterations = iterations

        sample_instance = PlantPropagation(bench, bounds, 10000, **{"m":20, "max_runners":5})
        pop_fitness = [point.fitness for point in sample_instance.population]
        sample_mean = np.mean(pop_fitness)

        bests = []
        for repetition in range(1, reps + 1):
            PPA_instance = PlantPropagation(self.bench, self.bounds, 10000, **{"m":20, "max_runners":5})
            PPA_instance.start()
            _, curbest = PPA_instance.env.get_evaluation_statistics_best()
            bests.append(curbest[-1])
        self.worst_fitness = median(bests)/sample_mean
        self.prev_terms = copy.deepcopy(self.bench.a)
    
    def mutate(self):
        """
        1) pick one of the polynomial terms
        2) pick a random float between -1 and 1
        3) add the random float to the polynomial term
        """
        terms = self.bench.a

        # Pick random term from list of terms
        index = random.randrange(len(terms))
        term_to_mutate = terms[index]

        # Add mutation to the term
        mutation = np.random.uniform(-0.5, 0.5)
        term_to_mutate += mutation

        terms[index] = term_to_mutate
        self.bench.a = terms
        return

    def start(self, reps=10):
        """
        1) Mutate the initial benchmark function

        2) Assign fitnesss score
        2a) Random sample the function (10.000 evaluations)
        2b) Perform 10 (?) runs of PPA and take median best found value
        2c) Fitness = objective_value / random_sample_mean

        3) Mutate benchmark function
        4) Repeat step 2 and keep new function if fitness score is lower (i.e. function is harder)
        """
        params = {}
        print(self.prev_terms)
        for i in range(self.iterations):
            # Mutate benchmark function
            self.mutate()

            sample_instance = PlantPropagation(self.bench, self.bounds, 10000, **{"m":20, "max_runners":5})
            pop_fitness = [point.fitness for point in sample_instance.population]
            sample_mean = mean(pop_fitness)

            bests = []
            for repetition in range(1, reps + 1):
                PPA_instance = PlantPropagation(self.bench, self.bounds, 10000, **{"m":20, "max_runners":5})
                PPA_instance.start()
                _, curbest = PPA_instance.env.get_evaluation_statistics_best()
                bests.append(curbest[-1])

            fitness = median(bests)/sample_mean
            # Save new_bench as hardest benchmark instance
            if fitness > self.worst_fitness:
                self.worst_fitness = fitness
                self.prev_terms = copy.deepcopy(self.bench.a)
                # self.bounds = new_bounds
                print("worse")
            else:
                self.bench.a = copy.deepcopy(self.prev_terms)
            if i in [0, 10, 20, 50, 100, 200, 299]:
                params[i] = copy.deepcopy(self.bench.a)
            print(i, self.bench.a)


        for key, value in params.items():
            x = np.linspace(-3, 3, 30)
            y = np.linspace(-2, 2, 30)
            self.bench.a = value

            # Run the hardest benchmark and save to csv
            do_run(PlantPropagation, self.bench, 10000, {"m":20, "max_runners":5}, 10, version=key)

            X, Y = np.meshgrid(x, y)
            coords = zip(X, Y)
            Z = np.array([self.bench(coord, a=self.bench.a) for coord in coords])

            # Create figure and add axis
            fig = plt.figure(figsize=(8,6))
            ax = plt.subplot(111, projection='3d')

            # Remove gray panes and axis grid
            ax.xaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor('white')
            ax.yaxis.pane.fill = False
            ax.yaxis.pane.set_edgecolor('white')
            ax.zaxis.pane.fill = False
            ax.zaxis.pane.set_edgecolor('white')
            ax.grid(False)
            ax.set_zlim(-100, 200)
            # Remove z-axis)
            print("before plotting")
            # Plot surface
            plot = ax.plot_surface(X=X, Y=Y, Z=Z, cmap='YlGnBu_r', vmin=0, vmax=200)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            print("show now")
            plt.show()
            print(self.bench.a)

bench_fun = [getattr(benchmarks, fun) for fun in dir(benchmarks) if hasattr(getattr(benchmarks, fun), 'is_n_dimensional')]
two_dim_fun = [fun for fun in bench_fun if not fun.is_n_dimensional]

func = two_dim_fun[1]
func.dims = 2
print(func.__name__)
Hillclimber(func, func.bounds, 2000).start()
