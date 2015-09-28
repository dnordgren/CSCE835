#!/usr/bin/perl -w

&go ();

sub go {
	my $s = `pwd`;
	warn "$s";	
	my $out = $s."/output.flv";
	$out =~ s/\n//g ;
#warn "$out";
	`ffmpeg -i input.mp4 -ar 22050 -crf 28 $out`;
}
