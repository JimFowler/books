<?php require '/home/jrf/private_html/phpBooks.inc';?>
<html> 
 <head>
<Title>Useful (or not) Blogs</Title>
 </head>
 <body>
 <?php BooksTop( "Books20:<br>The Blog List" ) ?>
 <P>
 <table>
    <tr valign="Top">
      <td width=250 height=250 valign="Top">
      	  <?php echo LoadPrivateFile( "BlogLists.txt")    ?> </td>
    </tr>
    </tr>


  </table>
 </body>
</html>
