#!/bin/sh
#SBATCH --ntasks=3
#SBATCH --time=03:15:00
#SBATCH --job-name=group8-hw8
#SBATCH --error=err.err
#SBATCH --output=out.out
mpiexec -n 3 python ~/CSCE835/hw8/gol.py -i sample.input -d
