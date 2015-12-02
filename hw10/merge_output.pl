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
  print "Sum is: $sum\n";
  my $duration = time - $start;
  print "Execution time: $duration s\n"; 
