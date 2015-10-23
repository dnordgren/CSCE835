#!/bin/sh
#SBATCH --ntasks=4
#SBATCH --time=03:15:00          # Run time in hh:mm:ss
#SBATCH --job-name=hw7
#SBATCH --error=hw7_2.err
#SBATCH --output=hw7_2.out

mpirun non_blocking
