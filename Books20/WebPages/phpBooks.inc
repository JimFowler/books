<?php
   function LoadFile( $inName ) {
     if ($theFile = fopen($inName, 'r')) {
       $theOutput = fread( $theFile, filesize($inName));
       fclose($theFile);
     } else {
       $theOutput = "Can not load $inName";
     }

     return $theOutput;
   }
?>

<?php function LoadPrivateFile( $inName ) {
      $privateName = '/home/jrf/private_html/' . $inName;
      return LoadFile( $privateName );
  }
?>


<?php
   function BooksTop( $inTitle ) {
     echo "<table>
      <tr>
        <td><img  width=285 height=168 src=\"./Images/bookrow.jpg\"></td>
        <td><h1>";
         echo "<center> $inTitle </center>";
         echo "</h1></td> 
      </tr>
    </table>";

    return;
   }
?>
