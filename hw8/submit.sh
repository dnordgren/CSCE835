#!/bin/bash
# call this script with the following parameters:
#     input file
#     number of cores to run the job with

# build the slurm file
echo "#!/bin/sh"                 > hw8.slurm
echo "#SBATCH --ntasks=$2"      >> hw8.slurm
echo "#SBATCH --time=03:15:00"  >> hw8.slurm
echo "#SBATCH --job-name=group8-hw8"    >> hw8.slurm
echo "#SBATCH --error=err.err"  >> hw8.slurm
echo "#SBATCH --output=out.out" >> hw8.slurm
echo "mpiexec -n $2 python ~/CSCE835/hw8/gol.py -i $1" >> hw8.slurm

# queue the slurm job
sbatch hw8.slurm

echo "check 'out.out' for results once the slurm job has completed"

exit 0
