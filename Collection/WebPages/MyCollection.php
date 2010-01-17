<?php
/*
  MyCollection.php

  The main web page for accessing my collection of books.

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

  BooksTop( 'My Book Collection' );

/*
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
*/

  echo '<table>
    <tr valign="Top"><td>';

  NavigationBar();

  echo '</td><td><table class="Books"><tr><td>';

  print "This is the main page for the Collection web site.
Start your navigation here.  You might even be able to login
sometime in the future. Start by searching for Title and/or Author,
Keywords (text fields, comments, title) or login to enable
the Add... buttons";

  echo '<br>';
  echo '<form action="searchresult.php" method="POST">';
 
  echo "</td></tr></table></table>\n";


  EndBookBody();
  EndBookHtml();

?>
