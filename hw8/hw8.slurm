#!/bin/sh
#SBATCH --ntasks=6
#SBATCH --time=03:15:00
#SBATCH --job-name=group8-hw8
#SBATCH --error=err.err
#SBATCH --output=out.out
mpiexec -n 6 python ~/CSCE835/hw8/gol.py -i sample.input
