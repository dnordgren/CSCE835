mkdir output_flv
for i in `cat files2`; do mv job_$i/output.flv output_flv/$i.flv; done
