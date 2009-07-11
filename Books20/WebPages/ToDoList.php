<?php require '/home/jrf/private_html/phpBooks.inc';?>
<html> 
 <head>
 <Title>Books20: To Do List</Title>
 </head>

 <body>
   <?php BooksTop( "Books20:<br>Dumb Things I Gotta Do" ) ?>
   <P>
   <table>
     <tr valign="Top">
       <td valign="Top">
      	  <?php echo LoadPrivateFile( "ToDoList.txt")    ?> </td>
     </tr>
   </table>
 </body>
</html>
