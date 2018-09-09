<?php include 'phpBooks.inc';?>
 <!-- Begin Copyright

  /home/jrf/Documents/books/Books20/WebPages/Bibliographies.php
  
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
 <Title>Bibliographies and References</Title>
 </head>
 <body>
 <?php BooksTop( "Books20:<br>Bibliography" ) ?>
 <P>
 <table>
    <tr valign="Top">
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "BibSources.txt")    ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "BibTools.txt")    ?> </td>
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "BibRefs.txt")    ?> </td>
    </tr>
    </tr>


  </table>
 </body>
</html>
