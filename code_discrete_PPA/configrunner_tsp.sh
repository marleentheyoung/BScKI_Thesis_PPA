#!/bin/bash
#Set job requirements
#SBATCH -N 1 
#SBATCH -t 12:30:00

#Loading modules
module load 2019
module unload Python
module load Python/3.6.6-intel-2019b 

#Run program
python code/config_runner_lisa.py data/PlantPropagation2_TSP data/cross