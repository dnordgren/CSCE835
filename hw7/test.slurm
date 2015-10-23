#!/bin/sh
#SBATCH --time=03:15:00          # Run time in hh:mm:ss
#SBATCH --nodes=3
#SBATCH --job-name=hw7
#SBATCH --error=hw7.err
#SBATCH --output=hw7.out

hostname
