#!/bin/sh
#SBATCH --ntasks=6
#SBATCH --time=03:15:00          # Run time in hh:mm:ss
#SBATCH --job-name=hw8
#SBATCH --error=err.err
#SBATCH --output=out.out

mpiexec -n 4 python ~/CSCE835/hw8/gol.py -i ~/CSCE835/hw8/sample.input -d
echo 'out.out'

