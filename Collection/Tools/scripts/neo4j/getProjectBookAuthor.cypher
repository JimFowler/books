// :params {projectName:'Mars', yearStart: 1900, yearEnd: 2020}
MATCH (p:Project)<-[:IN_PROJECT]-(b:Book)
WHERE p.name = $projectName
      AND $yearStart <= toInteger(b.copyright) <= $yearEnd
      UNWIND b as book
MATCH (book)<-[ao:AUTHOR_OF]-(author:Person)
WITH book, author, ao
ORDER BY ao.priority
RETURN book.title AS Title,
       collect(author.lastName + ', ' + author.firstName) AS Author,
       book.copyright AS Copyright
ORDER BY book.copyright;

       
