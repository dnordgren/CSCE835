ls -1 ../videos > files2
echo "executable = CSE835_HW4_part2.sh" > HW4_2.condor
echo "universe = vanilla" >> HW4_2.condor
echo "input = input.mp4" >> HW4_2.condor
echo "output = output.flv" >> HW4_2.condor
echo "log = log" >> HW4_2.condor
echo "error = error " >> HW4_2.condor
echo "" >> HW4_2.condor

for i in `cat files2`;do  echo "InitialDir = job_$i" >> HW4_2.condor; echo "queue" >> HW4_2.condor; echo "" >> HW4_2.condor ;done

condor_submit_dag hw4.dag

 
