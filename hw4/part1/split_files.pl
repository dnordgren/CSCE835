#!/usr/bin/perl -w
#use Getopt::Long;

&go ();

sub go {
    my $start = time;	
    my $f = "homework2.txt"; # change it when use for a diff file.
   
    my $n = `wc -l $f | perl -pe 's/^ +//g;chomp'`;
    my ($sum , $x) = split(/\ /,$n);
    my $node = 12;

    my $line = int($sum/$node);
    my $last = $sum - ($node - 1) * $line; 
    print "Splitting the input for parallelization ...\n";
    &partition($line, $last, $node, $f);
    &run($node, $start);
}

sub partition {
   my ($line, $last, $node, $f) = (@_);
   my $last_file_num = $node - 1;
   my $suffix = "";
   if($last_file_num < 10){
     $suffix = "0".$last_file_num;
   } else {
     $suffix = $last_file_num;
   }
  `split -l $line -a 2 -d $f input_`;
   my $x = ""; 
   if($node > 8){
      $x = $last_file_num + 1;
   }else{
     $x = "0".($last_file_num + 1);
	}
   `cat input_$x >> input_$last_file_num`;
   `rm input_$x`;
}

sub run{
  my ($node, $start) = (@_);
  my $suffix = "";
  my $dir_num = $node - 1;
  for (my $i = 0; $i <= $dir_num; $i++){
      `mkdir -p "job_$i"`;
      if ($i < 10){
        $suffix = "0".$i;
      }else{
        $suffix = "$i";
      }
      `mv input_$suffix ./job_$i/input`
  }
}

