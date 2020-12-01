#!usr/bin/perl
use Lingua::EN::Inflexion;
use 5.010;
use warnings;
use strict;
use FindBin;
use Data::Dumper qw(Dumper);

# Untested: indef_article(), indefinite($count), cardinal(), ordinal()
my $functions = {nouns => ["is_plural", "is_singular", "plural", "singular"], 
                 verbs => ["is_plural", "is_singular", "is_past", "is_pres_part", "is_past_part", "plural", "singular", "past", "pres_part", "past_part"], 
                 adjectives => ["is_plural", "is_singular", "plural", "singular"]};
my @word_types = ("nouns", "verbs", "adjectives");
my @classes = ("Lingua::EN::Inflexion::Noun", "Lingua::EN::Inflexion::Verb", "Lingua::EN::Inflexion::Adjective");

for my $i (0..2){
   my $word_type = $word_types[$i];
   my $class = $classes[$i];

   # Run the default functions without any parameters
   for my $func (@{$functions->{$word_type}}){
      # Output file for modern
      open(FH_out, '>', "$FindBin::Bin/../perl_output/$word_type/modern/$func.txt") or die $!;
      # Output file for classical
      open(FH_out_classical, '>', "$FindBin::Bin/../perl_output/$word_type/classical/$func.txt") or die $!;
      
      # Input file
      open(FH_in, '<', "$FindBin::Bin/../words/$word_type.txt") or die $!;
      while(<FH_in>){
         chomp;
         print FH_out $class->new($_)->$func || "0", "\n";
         print FH_out_classical $class->new($_)->classical->$func || "0", "\n";
      }
      close(FH_in);
      close(FH_out);
      close(FH_out_classical);
   }

   # Run the default functions with parameters
   my @args = (1, 2, 3);
   for my $arg (@args){
      my @functions_with_args = ("plural", "singular");
      for my $func (@functions_with_args){
         # Output file for modern
         open(FH_out, '>', "$FindBin::Bin/../perl_output/$word_type/modern/$func\_$arg.txt") or die $!;
         # Output file for classical
         open(FH_out_classical, '>', "$FindBin::Bin/../perl_output/$word_type/classical/$func\_$arg.txt") or die $!;
         
         # Input file
         open(FH_in, '<', "$FindBin::Bin/../words/$word_type.txt") or die $!;
         while(<FH_in>){
            chomp;
            print FH_out $class->new($_)->$func($arg) || "0", "\n";
            print FH_out_classical $class->new($_)->classical->$func($arg) || "0", "\n";
         }
         close(FH_in);
         close(FH_out);
         close(FH_out_classical);
      }
   }
}
