#include <math.h>

input_file=$1
total_lines=$(wc -l $input_file | cut -f1 -d' ')
cores=12
((lines_per_file=(total_lines + cores - 1) / cores)) 
split -l $lines_per_file -d $input_file input_
#split -l $(( $( wc -l < $input_file ) + $cores - 1 / $cores)) -d $input_file input_
for num in {0..11}; do
	mkdir -p "job_$num"

	if [ "$num" -lt "10" ]
	then
		suffix="0$num"
	else
		suffix="$num"
	fi
	mv "input_$suffix" "job_$num/input"		
done
#divisor=$(echo "$total_lines/$cores" | bc -l)
#lines=`expr $`
#echo "$divisor"
#awk -v divisor1="$divisor" 'NR% divisor1==1 {i=0} {file = "input_" sprintf("%d", i) }{input = "input.in"} {system("mkdir \"" file "\"")} {print "cd " file} {print > input } {i = i+1}' $input_file
rm -f hw1.submit
touch hw1.submit
echo "executable = $2" >> hw1.submit
echo "universe = vanilla" >> hw1.submit
echo "input = input" >> hw1.submit
echo "output = output" >> hw1.submit
echo "log = log" >> hw1.submit
echo "error = error" >> hw1.submit
echo "InitialDir = job_\$(Process)" >> hw1.submit
echo "queue 12" >> hw1.submit


condor_submit hw1.submit
condor_q
condor_wait log
echo "All done!"
condor_q
