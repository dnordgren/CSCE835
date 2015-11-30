#!/usr/bin/perl -w

my $start = time;
&go ();

sub go {
    my $sum = 0;
    open(IN, "one_thousand.txt") or die "Cannot open input file$!\n";
    while (<IN>) {
        next if /^\#/;
        next unless /\w/;
        $line = $_;
        my $num = &getnum($line);
        $sum += $num;
    }
    close(IN);
    print "$sum\n";
}

sub getnum {
    my $s = shift;
    my $n = substr($s, 39, 3);
    return $n;
}
