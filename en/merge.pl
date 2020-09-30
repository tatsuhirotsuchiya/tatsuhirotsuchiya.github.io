#perl
# usage: perl merge.pl filename
#   filename.txt is the body that will be embedded into template.html.
# 日本語へん！
# 機能．template.html の <--include-->の部分に，inputfileを挿入する
use warnings;
# use strict;
use utf8;
use Encode;

if ($#ARGV < 0) {
  exit(1);
}

my $templatefile = "template.html";
my $inputfile = $ARGV[0] . ".txt";
my $outputfile = $ARGV[0] . ".html";

open(IN1, $templatefile); 
open(IN2, $inputfile);
open(OUT, "> " . $outputfile);

while (my $l1 = <IN1>) {
  if ($l1 =~ /\s*<--include-->\s*/) {
    while (my $l2 = <IN2>) {
      $l2 = Encode::decode("shiftjis", $l2); 
      print $l2; 
      print(OUT $l2);
    }
  }
  else {
    print(OUT $l1);
  }
}
close(IN1);
close(IN2);
close(OUT);
