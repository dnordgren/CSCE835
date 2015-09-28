#!/usr/bin/perl -w

&go ();

sub go {
    my $path = "/home/pi/CSCE835/hw4/part2.2";
    open(IN, "< $path/files2") or die "Cannot open input file$!\n";
    `mkdir -p output_flv`;
    while (<IN>) {
            next if /^\#/;
            next unless /\w/;
      $line = $_;
      chomp $line;
      $line=~ s/\..*//;
      `mv $path/job_$line/output.flv $path/output_flv/$line.flv`;
    }
    close(IN);
    `echo "" >> $path/run_time.txt`;
    `date >> $path/run_time.txt`;
}
