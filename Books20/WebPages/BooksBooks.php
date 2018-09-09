<?php include 'phpBooks.inc';?>
 <!-- Begin Copyright

  /home/jrf/Documents/books/Books20/WebPages/BooksBooks.php
  
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
 <Title>Books and More Books</Title>
 </head>
 <?php BooksTop( "Books, Books<br>& More Books" ) ?>
 <P>
 <table>
    <tr valign="Top">
      <td width=250 height=250 valign="Top"
      	  ><?php echo LoadPrivateFile( "HomeLibrary.txt") ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "Libraries.txt")    ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "BooksOnLine.txt")  ?> </td>
    </tr>

    <tr valign="Top">
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "BookStores.txt") ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "References.txt") ?> </td>
      <td width=250 height=250 valign="Top">		  
      	  <?php echo LoadPrivateFile( "BookMaking.txt") ?> </td>
    </tr>

    <tr valign="Top">
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "Collecting.txt") ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "Resources.txt") ?> </td>
      <td width=250 height=250 valign="Top">		  
      	  <?php echo LoadPrivateFile( "RareBooks.txt") ?> </td>
    </tr>

  </table>
 </body>
</html>
