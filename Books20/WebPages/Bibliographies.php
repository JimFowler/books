<?php require '/home/jrf/private_html/phpBooks.inc';?>
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
