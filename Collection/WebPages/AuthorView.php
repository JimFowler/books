<?php
/*
  AuthorView.php

  View the full information about an Author.

  The last known changes were checked in by $Author$
  in revision $LastChangedRevision$
  on $Date$

*/

  require '/home/jrf/private_html/phpBooks.inc';

  StartBookHtml();
  StartBookHead( 'Author Collection of JRF' );
  StyleSheet( 'Collection.css' );
  EndBookHead();
  StartBookBody();

  BooksTop( 'Author View' );


  echo "<table>
    <tr valign=\"Top\"><td>";

  NavigationBar();

  echo "</td><td>";

  /*
   Check input arguments
  */ 
  $authorid = $_POST['authorid'];

  if( $authorid < 1 ) {
    echo "<h3>No such author in the database</h3></td></table>\n";
    EndBookBody();
    EndBookHtml();
    return;
  }

  if ( !($link = mysql_connect( 'localhost', 'Reader', 'librarycard' )) ) {
    echo 'Unable to connect to localhost as Reader</td></table>';
    EndBookBody();
    EndBookHtml();
    return;
  }

  if ( !mysql_select_db( 'Collection', $link ) ) {
    echo 'Can not connect to the Collection database!</td></table>';
    EndBookBody();
    EndBookHtml();
    return;
  }


  $AuthorQuery = "SELECT * FROM Authors WHERE Authors.AuthorId = $authorid";

  $AuthorQueryFmBooks = "SELECT Authors.*, BookAuthor.AsWritten
 FROM Authors INNER JOIN
      (BookAuthor INNER JOIN Books ON Books.BookId = BookAuthor.BookId)
      ON Authors.AuthorId = BookAuthor.AuthorId
 WHERE Books.BookId = $bookid
 ORDER By BookAuthor.Priority";


  $BookQuery = "SELECT Books.Title, Books.Copyright
 FROM Books INNER JOIN BookAuthor ON BookAuthor.BookId= Books.BookId
 WHERE BookAuthor.AuthorId = $authorid
 ORDER By Books.Copyright";

  $books = mysql_query( $BookQuery );
  $author = mysql_query( $AuthorQuery );

  $AuthorRow = mysql_fetch_array( $author );

  mysql_close( $link );


/*
 Ok, lets build the display
*/

print "<i><b>$AuthorRow[FirstName] $AuthorRow[MiddleName] $AuthorRow[LastName]</b></i><br>\n";
print "<br><b>Born:</b> $AuthorRow[Born] <b>Died:</b> $AuthorRow[Died]<br><br>
<b>Comments:</b><br>$AuthorRow[Comments]<br><br>
<b>Books:</b><br>\n";

/*
 Display the Authors
*/
$count = 0;
while ( $BookRow = mysql_fetch_array( $books )) {
  $count++;
  print "&nbsp&nbsp&nbsp&nbsp $BookRow[Title],  $BookRow[Copyright]<br>\n";
  }

echo "</td></tr>
</table>\n\n";


  EndBookBody();
  EndBookHtml();

?>
