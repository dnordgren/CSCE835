date > run_time.txt
ls -1 videos | perl -pe 's/\.mp4//g' > files2
rm -f  HW4_2.condor
rm -fr job_*
rm -f hw4.dag.*
echo "executable = main_job.pl" > HW4_2.condor
echo "universe = vanilla" >> HW4_2.condor
echo "input = input.mp4" >> HW4_2.condor
#echo "output = output.flv" >> HW4_2.condor
echo "log = log" >> HW4_2.condor
echo "error = error " >> HW4_2.condor
echo "should_transfer_files = YES" >> HW4_2.condor
printf "transfer_output_files = " >> HW4_2.condor
for i in `cat files2`; do printf "job_$i/output.flv," >> HW4_2.condor; done
printf "\nwhen_to_transfer_output = ON_EXIT" >> HW4_2.condor
echo "" >> HW4_2.condor

for i in `cat files2`;do  echo "InitialDir = job_$i" >> HW4_2.condor; echo "queue" >> HW4_2.condor; echo "" >> HW4_2.condor ;done

condor_submit_dag hw4.dag

 
