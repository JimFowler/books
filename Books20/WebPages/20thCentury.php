<?php include 'phpBooks.inc';?>
<html> 
 <head>
 <Title>Books in 20th Century Astronomy</Title>
 </head>
 <body>
 <?php BooksTop( "Books20:<br>Important and Influential<br> Books in<br>20th Century Astronomy" ) ?>
 <P>
 <table>
    <tr valign="Top">
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "20thCentury.txt")    ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "Libraries.txt")    ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "References.txt") ?> </td>
    </tr>

    <tr valign="Top">
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "Collecting.txt") ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "Resources.txt") ?> </td>
      <td width=250 height=250 valign="Top">		  
      	  <?php echo LoadPrivateFile( "RareBooks.txt") ?> </td>
    </tr>

    <tr valign="Top">
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "HistoryAstronomy.txt")    ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "HistoryReading.txt") ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "HistoryPublishing.txt")  ?> </td>
    </tr>

    <tr valign="Top">
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "BooksOnLine.txt")  ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "SociologyScience.txt") ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "Tools.txt")  ?> </td>
    </tr>


  </table>
 </body>
</html>
