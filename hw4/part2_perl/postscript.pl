#!/usr/bin/perl -w

&go ();

sub go {
    open(IN, "< files2") or die "Cannot open input file$!\n";
    `mkdir -p output_flv`;
    while (<IN>) {
            next if /^\#/;
            next unless /\w/;
      $line = $_;
      chomp $line;
      $line=~ s/\..*//;
      `mv job_$line/output.flv output_flv/$line.flv`;
    }
    close(IN);
}
