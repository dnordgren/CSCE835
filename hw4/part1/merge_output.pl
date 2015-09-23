#!/usr/bin/perl

my $sum = 0;
  for (my $j = 0; $j <=11; $j++){
     #my $num = 0;
     open(FI, "< job_$j/output") or die "Cannot open output file$!\n";
	my $num = <FI>;
        #print "$num";
     close(FI);
    # my $num2 = &getnum($num);
     $sum = $sum + $num;		
  }
open (OF, "> final_res.txt") or die "cannot open final out file"; 
  print OF "Sum is: $sum\n";
close(OF);
#`cat final_res.txt`
#  my $duration = time - $start;
#  print "Execution time: $duration s\n"; 

