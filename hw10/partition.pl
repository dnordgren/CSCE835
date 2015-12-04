#!/usr/bin/perl -w
use Getopt::Long;


# my $start = time;
# my $node = 12;
&go ();

sub go {
    #my ($node, $start) = (@_);
    my $start = time;
    my $f = "$ARGV[0]"; # change it when use for a diff file.
    my $ex = $ARGV[1];
    my $n = `wc -l $f | perl -pe 's/^ +//g;chomp'`;
    my ($sum , $x) = split(/\ /,$n);
    my $node = 12;

    my $line = int($sum/$node);
warn "$line \t $node";
    my $last = $sum - ($node - 1) * $line;
    print "Splitting the input for parallelization ...\n";
    &partition($line, $last, $node, $f);
    &run($ex,$node,$start);
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
 #  print `wc -l $f`;
warn "$line\t$node";
  `split -l $line -a 2 -d $f input_`;
#    `tail -$last $f >  input_$last_file_num`;
   #`tail -$last -$f >> $last_file_num`;
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
  my ($ex, $node, $start) = (@_);
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
  open(OF, "> hw1.submit") or die "Cannot open submit file$!\n";
    print OF "executable = $ex\n";
    print OF "universe = grid\n";
    print OF "grid_resource = condor red.unl.edu red.unl.edu:9619\n";
    print OF "use_x509userproxy = true\n";
    print OF "input = input\n";
    print OF "output = output\n";
    print OF "log = log\n";
    print OF "error = error\n";
    print OF "InitialDir = job_\$(Process)\n";
    print OF "queue $node\n";
  close(OF);

   print "Submitting jobs ...\n";
  `condor_submit hw1.submit`;
#=begin comment
  my $done_check = 0;
  #sleep(30);
  while($done_check != 6){
     $done_check = `condor_q | wc -l`;
     sleep(1);
   }
  my $sum = 0;
  my $output_file_num = $node - 1;
  for (my $j = 0; $j <=$output_file_num; $j++){
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
#=end comment

#=cut
}
