<?php
/*
  booksView.php

  View the full information about a book.

  The last known changes were checked in by $Author$
  in revision $LastChangedRevision$
  on $Date$

*/

  require '/home/jrf/private_html/phpBooks.inc';

  StartBookHtml();
  StartBookHead( 'Book Collection of JRF' );
  StyleSheet( 'Collection.css' );
  EndBookHead();
  StartBookBody();

  BooksTop( 'Book View' );


  echo "<table>
    <tr valign=\"Top\"><td>";

  NavigationBar();

  echo "</td><td>";

  /*
   Check input arguments
  */ 
  $bookid = $_POST['bookid'];

  if( $bookid < 1 ) {
    echo "<h3>No such book in the database</h3></table>\n";
    EndBookBody();
    EndBookHtml();
    return;
  }

  if ( !($link = mysql_connect( 'localhost', 'Reader', 'librarycard' )) ) {
    echo 'Unable to connect to localhost as Reader</table>';
    EndBookBody();
    EndBookHtml();
    return;
  }

  if ( !mysql_select_db( 'Collection', $link ) ) {
    echo 'Can not connect to the Collection database!</table>';
    EndBookBody();
    EndBookHtml();
    return;
  }


  $BookQuery = "SELECT Books.*
 FROM Books
 WHERE Books.BookId = $bookid";

  $VendorQuery = "SELECT Vendors.*
 FROM Vendors INNER JOIN Books ON Vendors.VendorId = Books.PurchasedFrom
 WHERE Books.BookId = $bookid";

  $PublisherQuery = "SELECT Vendors.*
 FROM Vendors INNER JOIN Books ON Vendors.VendorId = Books.Publisher
 WHERE Books.BookId = $bookid";

  $AuthorQuery = "SELECT Authors.*, BookAuthor.AsWritten
 FROM Authors INNER JOIN
      (BookAuthor INNER JOIN Books ON Books.BookId = BookAuthor.BookId)
      ON Authors.AuthorId = BookAuthor.AuthorId
 WHERE Books.BookId = $bookid
 ORDER By BookAuthor.Priority";

  $book = mysql_query( $BookQuery );
  $vendor = mysql_query( $VendorQuery );
  $publisher = mysql_query( $PublisherQuery );
  $authors = mysql_query( $AuthorQuery );

  $BookRow = mysql_fetch_array( $book );
  $PublRow = mysql_fetch_array( $publisher );
  $VendRow = mysql_fetch_array( $vendor );

  mysql_close( $link );

/*
 Ok, lets build the display
*/



print "<i><b>$BookRow[Title]</b></i><br>";
/*
 Display the Authors
*/
$count = 0;
while ( $AuthRow = mysql_fetch_array( $authors )) {
  $count++;
  print "&nbsp&nbsp&nbsp&nbsp $AuthRow[3] $AuthRow[2] $AuthRow[1] as  $AuthRow[7]<br>\n";
  }

print "<br><b>Published:</b> $BookRow[PublishedAt], $PublRow[Name], $BookRow[Copyright]<br>
<b>Purchased:</b> $VendRow[Name],  $BookRow[PurchaseDate], \$$BookRow[PurchasePrice]<br>
<b>Description:</b><br> $BookRow[MyCondition], $BookRow[Description]<br>
<b>Comments:</b><br> $BookRow[Comments]<br></td></tr></table>\n";


  EndBookBody();
  EndBookHtml();

?>
