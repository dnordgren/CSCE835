#!/usr/bin/perl -w

&go ();

sub go {
    open(IN, "< files3") or die "Cannot open input file$!\n";
    while (<IN>) {
            next if /^\#/;
            next unless /\w/;
      $line = $_;
	$line=~ s/\..*//;
	chomp $line;
      `mkdir -p job_$line`;
      `cp ../videos/$line.mp4 job_$line/input.mp4`;
    }
    close(IN);
}
