<?php
/*
  phpBooks.inc

  A collection of php functions for the Books20
  and My Collection book databases.

  The last known changes were checked in by $Author$
  in revision $LastChangedRevision$
  on $Date$
*/

function StartBookHtml() {

  echo "<html>\n";

  /* add meta stuff here */
}

function EndBookHtml() {

  echo "</html>\n";

}

function StartBookHead( $Title ) {

  echo '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">';

  echo "\n<head>\n<title>$Title</title>\n";

  /* add scripts and style sheets here */
}

function EndBookHead() {

  echo "</head>\n";

}

function StartBookBody() {

  echo "<body>\n";

}
function EndBookBody() {

  echo "</body>\n";

}

/*

  StyleSheet

  Link to a particular style sheet.
*/
function StyleSheet( $file ) {

  echo '<link rel="stylesheet" type="text/css" href=';
  print '"' . $file . '"/>' . "\n";

}
  
function LoadFile( $inName ) {
  if ($theFile = fopen($inName, 'r')) {
    $theOutput = fread( $theFile, filesize($inName));
    fclose($theFile);
  } else {
    $theOutput = "Can not load $inName";
  }

  return $theOutput;
}



function LoadPrivateFile( $inName ) {
  $privateName = '../private_html/' . $inName;
  /*  return LoadFile( $privateName );*/
  include( $inName );
  return;
}


function BooksTop( $inTitle ) {
  echo "<table>
  <tr>
    <td><img  width=285 height=168 src=\"./Images/bookrow.jpg\"></td>
    <td><h1>";
      echo "<center> $inTitle </center>";
      echo "</h1></td> 
  </tr>
</table>\n";

    return;
}

/*
 NavigationBar

  Show the Books nvaigation bar.  Used in Collections
  for the time being.
*/
function NavigationBar () {

  echo '<ul class="navbar">
          <li> <a href="AllBooks.php">Books</a>
          <li> Wants
          <li> <a href="AllAuthors.php">Authors</a>
          <li> Publishers <br> and Vendors
          <li> <a href="AllProjects.php"">Projects</a>
          <li> Reports
        </ul>';
}

?>