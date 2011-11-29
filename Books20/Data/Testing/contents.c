/*
  contents.c

  Strip HTML tags out of the AJB table of contents.

  usage: contents < ajb61_contents.txt > ajb61_clean.txt


  History
    created 13 Nov 2011

*/

#include <stdio.h>
#include <stdlib.h>

#define Start_Char '<'
#define Stop_Char '>'
#define Tab_Char '\011'

int
main( int argc, char *argv )
{

  int c, output_f;
  
  c = 0;
  output_f = 1;

  while( EOF != (c = getchar()) )
    {
      if( Start_Char == c )
	{
	  output_f = 0;
	}
      else if( Stop_Char == c )
	{
	  output_f = 1;
	}
      else if( output_f )
	{
	  if( Tab_Char == c )
	    {
	      // put a comma and one space char
	      putchar(44); putchar(32);
	    }
	  else
	    {
	      putchar( c );
	    }
	}
    }

  exit(0);
}
   
