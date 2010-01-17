<?php
/*
  AllProjects.php

  The main web page for accessing the Project list in my collection of books.

  The last known changes were checked in by $Author$
  in revision $LastChangedRevision$
  on $Date$

*/

  require '/home/jrf/private_html/phpBooks.inc';

  StartBookHtml();
  StartBookHead( 'All Projects in the Collection of JRF' );
  StyleSheet( 'Collection.css' );
  EndBookHead();
  StartBookBody();

  BooksTop( 'Projects in My Collection' );


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


  $projectQuery = 'SELECT * FROM Projects ORDER BY Projects.ProjName';

  $projects = mysql_query( $projectQuery );

  mysql_close( $link );

  $NumRows = mysql_num_rows( $projects );

  print "<tr><td>&nbsp&nbsp&nbsp Total $NumRows</td></tr>\n";

  while ($row = mysql_fetch_array( $projects, MYSQL_BOTH )) {
    echo "<tr><td><hr></td></tr>\n";
    echo "<tr><td>
<form method=\"POST\" action=\"ProjectView.php\">
<input type=\"hidden\" name=\"projectid\" value=\"$row[ProjectId]\"> 
<input class=\"Title\" type=\"submit\"
      value=\"$row[ProjName]\" name=\"submit\">
</form></td></tr>\n";
  }

  echo "</table></td></tr></table>\n";


  EndBookBody();
  EndBookHtml();

?>
