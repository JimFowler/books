				  
MATCH (b:Book)<-[:AUTHOR_OF]-(author:Person)
WHERE b.publishedAt = $publishPlace
      AND $yearStart <= toInteger(b.copyright) <= $yearEnd
RETURN b.title AS Title,
       author.lastName + ', ' + author.firstName AS Author,
       b.copyright AS Copyright
ORDER BY b.copyright ;
