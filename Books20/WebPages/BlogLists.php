<?php require '/home/jrf/private_html/phpBooks.inc';?>
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
