Design of the Database
======================

Nodes
_____

Nodes may be indexed on their properties

The nodes may consist of the following labels,

  * :Series
    unique id, name,
    
  * :Book:MultiVolume
    unique id, title, [series/volume number], edition, language

  * :Book

  * :Person
    unique id, first, middle, last, born, died
    
  * :Corporate
    name, mail/ship address, url, email
    
  * :Journal
    name, start, end
    
  * :Review
  * :Project
  * :Bibliography - AJB, AAA, others?
  * :Year, :Month, :Day

    * properties: value, month_name, month_number

  * something for the AJB/AAA counts

Relationships
_____________

Remember that relationship can not be indexed. For faster searches
we should keep relationship properties to a minimum if we plan to make
decisions based on those properties.

The relationships may consist of,

  * :Book to :MultiVolume

    * :PART_OF {volume: n}
      
  * :Book to :Book
    
    * :EDITION_OF {edition: n}
	
    * :REPRINT_OF
    * :TRANSLATION_OF

  * :Book to :Person
    
    * :AUTHOR {authorNumber: n}	
    * :EDITOR {editorNumber: n}
    * :TRANSLATOR {translatorNumber: n}
    * :COMPILER {compilerNumber: n}
    * :CONTRIBUTER {contributorNumber: n}
    * :ILLUSTRATOR {illustratorNumber: n}

  * :Book to :Corporate
    
    * all of the book-to-people relations
    * :PRINTED_BY
    * :PUBLISHED_BY

      * properties: copyright:
	
    * :PURCHASED_FROM {purchaseYear:, purchasePrice:}
	
  * :Review
    
    * :OF_BOOK -> (:Book)
    * :IN_JOURNAL -> (:Journal {issue: n, page: m}
    * :REVIEWED_BY -> (:Person)
