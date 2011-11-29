#!/usr/bin/perl -w
#
# aaa_parse.pl
#
#  Parse the file of Books entries from Astronomy and Astrophyscs Abstracts.
#
#
#
#  |a|F._Hoyle, G._Burbidge, J._V._Narlikar
#  |t|A different approach to cosmology. 
#  |s|Cambridge (UK): Cambridge University Press, XI_+_357_p.
#  |y|2000
#  |k|Cosmological Models, Cosmology:Big-Bang Theory
#  |n|AAA073.003.001
#  |j|A._Schoedlbauer  A._Schodlbauer 
#
#
#The format of the lines in the files:
# * |a| author(s) or editor(s)
#
# * |t| title of the book/publication [contents within
#      brackets are additions from AJB/AAA and mostly translations
#
# * |s| source ( with the usual abbreviations )
#
# * |y| publication date/year
#
# * |k| keyword(s)
#
# * |n| registration count within ARIBIB: AAAvvv.sss.nnn
#      when from AAA: vvv = Volume / sss = Section / nnn = count within section
#
#  |i| LINK-address to the scanned image of the respective page =
#        registration count within ARIBIB:
#          AJBvvvpPPP/sss.nnnn  when from AJB:
#           vvv = Volume 
#           PPP = pagenumber within volume 
#           sss = Section 
#           nnn = count within section
#
#  |j| when author, title and/or source word contains natl. characters
#      (umlauts, accents, ...) then there is the 7bit-clean alternate search token 
#
# * |b| ADS bibcode reference
#
#  |l| unknown
#
#  There are never more than 9 of these fields though
#    there are 10 possible fields total.
#
#
package jrfAAA;

use warnings;
use strict;
use Getopt::Std;
use utf8;

#
# Declare and initialize variables
#
my ( $AAA_file, @AAAentries, $line, $linecounter, $lineskip );
my ( $field01, $field02, $field03, $field04, $field05 );
my ( $field06, $field07, $field08, $field09, $field10 );
my ( $field11, $field12, $field13, $field14, $field15 );
my ( $field16, $field17, $field18, $field19, $field20 );
my ( $index, $ajbnum, $authorstr, @Authors );
my ( %Publishers, $Publishers );
my ( $maxindex, $maxline );

my $usage = 
    "aaa.pl [-vdh] filename \n" .
    "        -v verbose option,\n" .
    "        -d include debug output,\n" .
    "        -h print this help message,\n" .
    "        filename may be '-' to use standard input.\n" .
    "\n";


%Publishers = ();


#
# Define subroutines
#



#
#
#  Main
#
# Ok, lets start the main stuff
#
#

use vars qw( $opt_v $opt_d $opt_h );

#
# Check command line
#
getopts( 'vdh' ) or die $usage;

die $usage if $opt_h;


#
# get number of lines to skip if on the command line
#
$lineskip = 0;
$linecounter = 0;


# verify filename has been provide

if ( ! $ARGV[0] ) {
    die "<filename> must be included on command line.\n\n$usage";
} elsif ( $ARGV[0] eq "-" ) {
    $AAA_file = "stdin";
} else {
    $AAA_file = $ARGV[0];
}

if ($opt_d) {
    print "filename is $AAA_file\n";
}

# verify file_name is readable
if ( "stdin" eq $AAA_file) {
    @AAAentries = <STDIN>;
} elsif ( -f $AAA_file ) {
    @AAAentries = `cat $AAA_file`;
} else {
    die "AAA file $AAA_file is not a readable file.\n";
}

$maxindex = 0;
$maxline = 0;
$linecounter = 1;

#
# Ok, let's get the entries
#
#
LINE:
foreach $line (@AAAentries) {

    chomp $line;

    #($field20, $field01, $field02, $field03, $field04, $field05,
    # $field06, $field07, $field08, $field09, $field10,
    # $field11, $field12, $field13, $field14, $field15,
    # $field16 )  = split /\|/, $line;

    #print "$field01 $field03 $field05 $field07 $field09 $field11 $field13 $field15\n";

    @Authors =  split( ?\|?, $line);
    print  "$Authors[1]  $Authors[2] $Authors[3] $Authors[4]\n";

    #
    # If we are not past the headers lines or field02 is empty (no title)
    # or field01 is not of the correct pattern we reject the line and move on
    #
    next LINE if ( (++$linecounter < $lineskip) 
		   || !$field02 || !($field01 =~ m/[0-9]+/x) );

    #
    # Parse the fields
    #

    #
    # Get rid of leading/trailing spaces and
    #   parse field 01 to get index, AJB number, and author array
    #
    # This is not portable outside the LINE block
    #
    #$field01 =~ s/^\s+|\s+$//;
    #($index, $ajbnum, $authorstr) = split " ", $field01, 3;
    #if( $authorstr ) {
	#$authorstr =~ s/^\s+|\s+$//;
	#@Authors = split " and ", $authorstr;
    #} else {
	#@Authors = "";
    #}

    #if( $opt_d && @Authors) {
	#my $aentry;
	#print "Entry $index has AJBnum $ajbnum and authors\n";
	#foreach  $aentry (@Authors) {
	#    print "$aentry\n";
	#}
    #}


    #
    # remove leading/trailing spaces and parse field 04 for publisher
    #  if publisher is empty 
    #     add line to hash table under NoPublisher
    #  else
    #     add AJBnum to line under Publisher
    #
    #$field04 =~ s/^\s+//;
    #$field04 =~ s/\s+$//;

    #if( !$field04 || $field04 eq "" ) {
	#$field04 = "NoPublisher";
    #}
    #if ( $Publishers{$field04} ) {
	#$Publishers{$field04} = join " ", $Publishers{$field04}, $ajbnum;
    #} else {
	#$Publishers{$field04} = $ajbnum;
    #}


}
#
# End of LINE
#


#print "Publishers:\n";
#if ($opt_d ) {
#    my ( $pkey );
#    
#    foreach $pkey (sort keys %Publishers) {
#	print  "$pkey: entries: $Publishers{$pkey}\n";
#    }
#}
	    
	    
