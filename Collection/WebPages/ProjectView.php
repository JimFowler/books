<?php
/*
  ProjectView.php

  View the full information about a Project

  The last known changes were checked in by $Author$
  in revision $LastChangedRevision$
  on $Date$

*/

  require '/home/jrf/private_html/phpBooks.inc';

  StartBookHtml();
  StartBookHead( 'Projects Collection of JRF' );
  StyleSheet( 'Collection.css' );
  EndBookHead();
  StartBookBody();

  BooksTop( 'Project View' );


  echo "<table>
    <tr valign=\"Top\"><td>";

  NavigationBar();

  echo "</td><td>";

  /*
   Check input arguments
  */ 
  $projectid = $_POST['projectid'];

  if( $projectid < 1 ) {
    echo "<h3>No such project in the database</h3></td></table>\n";
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


  $ProjectQuery = "SELECT * FROM Projects WHERE Projects.ProjectId = $projectid";

  $AuthorQueryFmBooks = "SELECT Authors.*, BookAuthor.AsWritten
 FROM Authors INNER JOIN
      (BookAuthor INNER JOIN Books ON Books.BookId = BookAuthor.BookId)
      ON Authors.AuthorId = BookAuthor.AuthorId
 WHERE Books.BookId = $bookid
 ORDER By BookAuthor.Priority";


  $BookQuery = "SELECT Books.Title, Books.Copyright
 FROM Books INNER JOIN BookProject ON BookProject.BookId= Books.BookId
 WHERE BookProject.ProjectId = $projectid
 ORDER By Books.Copyright";

  $books = mysql_query( $BookQuery );
  $project = mysql_query( $ProjectQuery );

  mysql_close( $link );


  $ProjectRow = mysql_fetch_array( $project );
  $BookCount = mysql_num_rows( $books );


/*
 Ok, lets build the display
*/

print "<i><b>$ProjectRow[ProjName]</b></i><p>\n";
print "<b>Description:</b><br>$ProjectRow[Description]<br><br>
<b>Books:</b> (total $BookCount)<br>\n";

/*
 Display the Books
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
