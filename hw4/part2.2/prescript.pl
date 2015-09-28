#!/usr/bin/perl -w

&go ();

sub go {
    my $path = "/home/pi/CSCE835/hw4/part2.2";
    warn "$path/files2";
    open(IN, "< $path/files2") or die "Cannot open input file$!\n";
    while (<IN>) {
            next if /^\#/;
            next unless /\w/;
      $line = $_;
	$line=~ s/\..*//;
	chomp $line;
      `mkdir -p $path/job_$line`;
      `cp $path/videos/$line.mp4 $path/job_$line/input.mp4`;
    }
    close(IN);
}
