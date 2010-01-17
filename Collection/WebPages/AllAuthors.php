<?php
/*
  AllAuthors.php

  The main web page for accessing the Author list in my collection of books.

  The last known changes were checked in by $Author$
  in revision $LastChangedRevision$
  on $Date$

*/

  require '/home/jrf/private_html/phpBooks.inc';

  StartBookHtml();
  StartBookHead( 'All Authors in the Collection of JRF' );
  StyleSheet( 'Collection.css' );
  EndBookHead();
  StartBookBody();

  BooksTop( 'Authors in My Collection' );


  echo "<table>
    <tr valign=\"Top\"><td>";

  NavigationBar();

  echo "</td><td><table class=\"Books\">
         <tr><td><b>Name</b></td></tr>\n";

/*
 Ok, get the Books data
*/
  if ( !($link = mysql_connect( 'localhost', 'Reader', 'librarycard' )) ) {
    echo 'Unable to connect to localhost as Reader';
    EndBookBody();
    EndBookHtml();
    return;
  }

  if ( !mysql_select_db( 'Collection', $link ) ) {
    echo 'Can not connect to the Collection database!';
    EndBookBody();
    EndBookHtml();
    return;
  }


  $authorQuery = 'SELECT * FROM Authors ORDER BY Authors.LastName';

  $authors = mysql_query( $authorQuery );

  mysql_close( $link );

  $NumRows = mysql_num_rows( $authors );

  print "<tr><td>&nbsp&nbsp&nbsp Total $NumRows</td></tr>\n";

  while ($row = mysql_fetch_array( $authors, MYSQL_BOTH )) {
    echo "<tr><td><hr></td></tr>\n";
    echo "<tr><td>
<form method=\"POST\" action=\"AuthorView.php\">
<input type=\"hidden\" name=\"authorid\" value=\"$row[AuthorId]\"> 
<input class=\"Title\" type=\"submit\"
      value=\"$row[FirstName] $row[MiddleName] $row[LastName]\" name=\"submit\">
</form></td></tr>\n";
  }

  echo "</table></td></tr></table>\n";


  EndBookBody();
  EndBookHtml();

?>
