<?php include 'phpBooks.inc';?>
 <!-- Begin Copyright

  /home/jrf/Documents/books/Books20/WebPages/20thCentury.php
  
   Part of the Books20 Project

   Copyright 2018 James R. Fowler

   All rights reserved. No part of this publication may be
   reproduced, stored in a retrival system, or transmitted
   in any form or by any means, electronic, mechanical,
   photocopying, recording, or otherwise, without prior written
   permission of the author.


 End Copyright -->


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
