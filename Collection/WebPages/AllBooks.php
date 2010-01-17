<?php
/*
  AllBooks.php

  The main web page for accessing my collection of books.

  The last known changes were checked in by $Author$
  in revision $LastChangedRevision$
  on $Date$

*/

  require '/home/jrf/private_html/phpBooks.inc';

  require 'connection.php';
  require 'MySQLConnect.php';
  require 'PageNavigator.php';

  //max per page
  define("PERPAGE", 50);

  //get query string
  $offset=@$_GET['offset'];
  //check variable
  if (!isset($offset)){
    $recordoffset = 0;
  }else{
    //calc record offset
    $recordoffset = $offset*PERPAGE;
  }


  StartBookHtml();
  StartBookHead( 'All Books in the Collection of JRF' );
  StyleSheet( 'Collection.css' );
  EndBookHead();
  StartBookBody();

  BooksTop( 'Books in My Collection' );


  echo "<table>
    <tr valign=\"Top\">\n      <td>";

  NavigationBar();

echo "</td>\n      <td>";


  /*
   Ok, try to get the Books data
  */
try {
  $con = new MySQLConnect($hostname, $username, $password); 

  $bookQuery = 'SELECT Books.BookId, Books.Title, Books.Copyright, Authors.LastName
      FROM Books INNER JOIN
             (Authors INNER JOIN BookAuthor ON Authors.AuthorId = BookAuthor.AuthorId)
              ON Books.BookId = BookAuthor.BookId
      WHERE (BookAuthor.Priority = 1) 
      ORDER BY Authors.LastName LIMIT ' . $recordoffset . ', ' . PERPAGE;

  $books = $con->createResultSet($bookQuery, $databasename);

  $pagename = basename($_SERVER['PHP_SELF']);
  // Do some calcuations about the record set
  $totalrecords = $books->getUnlimitedNumberRows();
  $numpages = ceil($totalrecords/PERPAGE);
  $firstrecord = $recordoffset + 1;
  $lastrecord = $recordoffset + PERPAGE;
  if($lastrecord > $totalrecords) {
    $lastrecord = $totalrecords;
  }

  echo "<table class=\"Books\">";
  echo "<tr>\n     <td><B>Displaying $firstrecord - $lastrecord  of $totalrecords Books</B></td>\n";

  //create if needed  
  if($numpages > 1)  {
    //create navigator
    $nav = new PageNavigator($pagename, $totalrecords, PERPAGE, 
			$recordoffset, 4, $otherparameter);
    echo '<td>';
    echo $nav->getNavigator();
    echo '</td></tr></table>';
  } else {
    echo '</tr></table>';
  }

  echo "<table class=\"Books\">";
  echo "<tr><td><b>Title</b></td><td><b>Author</b></td><td><b>Copyright</b></td></tr>\n";

  foreach($books as $row ) {
    echo "<tr><td colspan=\"3\"><hr></td></tr>\n";
    echo "<tr><td>
<form method=\"POST\" action=\"BookView.php\">
<input type=\"hidden\" name=\"bookid\" value=\"$row[BookId]\"> 
<input class=\"Title\" type=\"submit\" value=\"$row[Title]\" name=\"submit\">
</form></td><td>$row[LastName]</td><td>$row[Copyright]</td></tr>\n";
  }

  echo "</td></tr></table></table>\n";

  EndBookBody();
  EndBookHtml();

  //create if needed  
  if($numpages > 1)  {
    //alread created navigator
    echo '<center>';
    echo $nav->getNavigator();
    echo '</center>';
  }
}
catch(Exception $e) {

  echo $e;
  EndBookBody();
  EndBookHtml();
}

    
?>
