<?php include 'phpBooks.inc';?>
 <!-- Begin Copyright

  /home/jrf/Documents/books/Books20/WebPages/BlogLists.php
  
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
<Title>Useful (or not) Blogs</Title>
 </head>
 <body>
 <?php BooksTop( "Books20:<br>The Blog List" ) ?>
 <P>
  <table>
      	  <?php echo LoadPrivateFile( "BlogLists.txt")    ?>
  </table>
 </body>
</html>
