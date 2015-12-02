#!/usr/bin/perl -w

my $start = time;
&go ();

sub go {
    my $sum = 0;
    open(IN, "<input") or die "Cannot open input file$!\n";
    while (<IN>) {
	    next if /^\#/;
	    next unless /\w/;
      $line = $_;
      my $num = &getnum($line);
      $sum += $num;
    }
    close(IN);
    print "$sum\n";
    #my $duration = time - $start;
    #print "Execution time: $duration s\n";
}

sub getnum {
    my $s = shift;
    my $max = 0;
    #my @ss;
    for (my $i = 0; $i <= length($s)-2; $i++){
      my $n = substr($s, $i, 3);
      if ($n > $max){
        $max = $n;
      }
    }

   # print "$max\t";
    return $max;
}
