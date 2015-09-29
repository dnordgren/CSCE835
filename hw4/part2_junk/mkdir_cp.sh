!#/bin/bash

for i in `cat files2`; do mkdir job_$i; cp /home/pi/CSCE835/hw4/part2/videos/$i ./job_$i/input.mp4; done

 
