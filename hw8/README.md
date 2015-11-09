### Group 8, HW 8
Author: Derek Nordgren

To run, execute the shell script `submit.sh` as follows:
`$ sh submit.sh <input_file> <num_of_cores>`

This script builds the necessary slurm file and batches a slurm job.

It then prints the location of the output file. The output file will be ready once
the slurm job has finished.

For more robust output, within the slurm file, append a `-d` flag to the end of
the `mpiexec` command like so:
`mpiexec -n 6 python ~/CSCE835/hw8/gol.py -i sample.input -d`

It is assumed the the user will change the Python script in the above command to
match where the script lives on their machine.
