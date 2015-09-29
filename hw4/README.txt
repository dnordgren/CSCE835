Part 1
	So to verify that our Part 1 with DAGMan completed successfully, check that
	part1/final_res.txt contains the correct answer from the previous homework.

	If you want to run part1, simply execute 'condor_submit_dag hw4.dag' in part1/.


Part 2
	2.1 - Full NFS
	---------------------------------------------------------------------------------------------
	We executed the ffmpeg jobs first using NFS, which took approximately 9 minutes (see 
	part2.1/NFS_run_time.txt for exact timestamps).

	To execute this, run the command `bash part2.1/init.sh`. The output will be stored in run_time.txt.
	
	2.2 - Half NFS
	---------------------------------------------------------------------------------------------
	In this part we used input through NFS and transferred the output. To make sure input is through NFS,
	we hard coded absolute path to the files in the scipts.
 
	This part took approximately 9 mins. See part2.2/run_time.txt for exact timestamps.

	To execute this, run the command `bash part2.2/init2.sh`.

	2.3 - No NFS
	---------------------------------------------------------------------------------------------
	In this part we turned off nfs and tranferred both the input and output files. This took approximately
	17 mins.
	
	To execute this, run the command `bash part2.3/init3.sh`. The start time will be stored in run_time.txt
	and the end time will be stored in run_time_output.txt

	Conclusion:
	We  have observed that NFS gives the best performance and Half NFS gives the next best.
	No NFS took significantly more time.
		
** Note **
	- We faced issues with dagman where it started the postscript when it saw the last job finish even though
	other jobs were still running. Similar issue was observed even after using PARENT CHILD paradigm of DAGMan.
	So we assume and approximately checked and added 2 mins to the runtimes obtained by the script.

	- For the testing the scripts, make sure videos folder containing the input videos is in part2.1/, part2.2/
	and part2.3. Similarly, the homework2.txt is present in part1/. We have not submitted these files due to the size.
	
	- Some places contain hardcoded path which was needed to use NFS on workers. This may cause some inconvience and
	debugging to run the scripts on a different environment. Sorry for the inconvience.
	
	
