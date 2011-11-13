#!/usr/bin/perl -w
#
# ajb_parse.pl
#
#  Parse the file of Books entries from Astronomischer JahresBericht.
#
#
#
#
#   Index AJB_Num Author, Title, Place, Publisher, Year,
#   Pagination, Price, Reviews, Comments
#
#
#   Field 1 Index AJB_Num Author has format
#
#    Index AJB_Num [I. A. Author [ and H. E. Another [and ...]]] \
#     [ed.|comp.|something else]
#
#   Field 2 Title
#
#   Field 3 Place
#
#     [name | name-name[-name[-...]] Name may contain spaces
#
#   Field 4 publisher
#
#   Field 5 Year
#
#   Field 6 Pagination
#
#   Field 7 Price
#
#   Field 8 Reviews
#
#     [Journal vol page [and Journal vol page [and ...]]]
#
#     Need to pull the Journal and reference from here
#
#   Field 9 Comment
#
#     Need to do something with these contains editions, editors,
#      translators, and other people
#
#
#
#
#
package jrfAJB;

use warnings;
use strict;
use Getopt::Std;
use utf8;

#
# Declare and initialize variables
#
my ( $AJB_file, @AJBentries, $line, $linecounter, $lineskip );
my ( $field01, $field02, $field03, $field04, $field05 );
my ( $field06, $field07, $field08, $field09 );
my ( $index, $ajbnum, $authorstr, @Authors );
my ( %Publishers, $Publishers );


my $usage = 
    "ajb.pl [-vdh] filename \n" .
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
$lineskip = 13;
$linecounter = 0;


# verify filename has been provide

if ( ! $ARGV[0] ) {
    die "<filename> must be included on command line.\n\n$usage";
} elsif ( $ARGV[0] eq "-" ) {
    $AJB_file = "stdin";
} else {
    $AJB_file = $ARGV[0];
}

if ($opt_d) {
    print "filename is $AJB_file\n";
}

# verify file_name is readable
if ( "stdin" eq $AJB_file) {
    @AJBentries = <STDIN>;
} elsif ( -f $AJB_file ) {
    @AJBentries = `cat $AJB_file`;
} else {
    die "AJB file $AJB_file is not a readable file.\n";
}


#
# Ok, let's get the entries
#
#
LINE:
foreach $line (@AJBentries) {

    chomp $line;

    ($field01, $field02, $field03, $field04, $field05,
     $field06, $field07, $field08, $field09)  = split ",", $line;

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
    $field01 =~ s/^\s+|\s+$//;
    ($index, $ajbnum, $authorstr) = split " ", $field01, 3;
    if( $authorstr ) {
	$authorstr =~ s/^\s+|\s+$//;
	@Authors = split " and ", $authorstr;
    } else {
	@Authors = "";
    }

    if( $opt_d && @Authors) {
	my $aentry;
	print "Entry $index has AJBnum $ajbnum and authors\n";
	foreach  $aentry (@Authors) {
	    print "$aentry\n";
	}
    }


    #
    # remove leading/trailing spaces and parse field 04 for publisher
    #  if publisher is empty 
    #     add line to hash table under NoPublisher
    #  else
    #     add AJBnum to line under Publisher
    #
    $field04 =~ s/^\s+//;
    $field04 =~ s/\s+$//;

    if( !$field04 || $field04 eq "" ) {
	$field04 = "NoPublisher";
    }
    if ( $Publishers{$field04} ) {
	$Publishers{$field04} = join " ", $Publishers{$field04}, $ajbnum;
    } else {
	$Publishers{$field04} = $ajbnum;
    }


}
#
# End of LINE
#


print "Publishers:\n";
if ($opt_d ) {
    my ( $pkey );
    
    foreach $pkey (sort keys %Publishers) {
	print  "$pkey: entries: $Publishers{$pkey}\n";
    }
}
	    
	    
