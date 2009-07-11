#!/usr/bin/perl
#
#
#  Algorithm to get records from Astronomy and Astrophysics Abstracts.
#
#
# The last known changes were checked in by $Author$
# as revision $LastChangedRevision$
# on $Date$
#
#
use HTTP::Client
require "timelocal.pl";


#
# Global variables
#
$StartVol = 1;
$EndVol = 73;

$MaxIndex = 300;

#
# Usage description
#
sub Usage() {

    print "Usage: aribib [startvol [endvol]]\n";
    print "          get bib entries from AAA volumes,\n";
    print "          volumes between 1 and 73,\n";
    print "          startvol alone gets only that volume,\n";
    print "          if no arguments, get volumes 1 through 73 inclusive.\n";
    print "\n";

}

#
# Check command line arguments
#
sub ParseArgs() {

    if( $#ARGV > -1 ) {

	$StartVol = $ARGV[0];
	$EndVol = $StartVol;
    }

    if( $#ARGV > 0 ) {
	$EndVol = $ARGV[1];
    }

    if( $#ARGV > 1 ) {
	Usage();
	exit();
    }

    if( 1 > $StartVol || 73 < $StartVol ) {
	print "Error: Starting volume value $StartVol is invalid\n";
	print "       value must be between 1 and 73 inclusive\n";
	Usage();
	exit();
    }

    if( 1 > $EndVol || 73 < $EndVol ) {
	print "Error: Ending volume value $EndVol is invalid\n";
	print "       value must be between 1 and 73 inclusive\n";
	Usage();
	exit();
    }

    if( $StartVol > $EndVol ) {
	print "Error: Starting volume ($StartVol) must be less than\n";
	print "       or equal to the ending volume ($EndVol).\n";
	Usage();
	exit();
    }
}




sub Main() {

    ParseArgs();

    print "Start Volume is $StartVol\n";
    print "  End Volume is $EndVol\n";

    for( $Vol = $StartVol; $Vol <= $EndVol; $Vol++ ) {

	print "   getting volume $Vol\n";
#
#    open "AAAvol.txt"
#     perror and continue if can't
#
	for( $Index = 1; $Index <= $MaxIndex; $Index++ ) {
#
#     reply = http://www.ari.uni-heidelberg.de/cgi-bin/aribib/aribib?showrec=AAA.vol.003.index;
#
#     if !grep "</html>" reply {   # not a complete reply
#     	index--;
#	continue;  # try again
#     } else if grep "ARIBIB error" reply {
#        close "AAAvol.txt"
#     	break;  # end of this volume
#     } else {
#       info = parse reply
#       write "AAAvol.txt" info
#     }
#     sleep 600 # 5 minutes
#  
	}		     # end of for index ...
#
#   write "AAAvol.txt" "Did not find end"
#
#   close "AAAvol.txt"
    }				# end of for vol...

} # end of Main()

#
# Ok, now that we have described everything we can do actual work
#
Main();


#
# spot comparison to the paper volumes
#
