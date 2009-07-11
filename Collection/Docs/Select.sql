-- DROP VIEW label;
-- CREATE VIEW label(written, title, priority) AS
SELECT * FROM Authors INNER JOIN BookAuthor ON (Authors.AuthorId=BookAuthor.AuthorId);
--  USING(AuthorId);


-- SELECT BookAuthor.AsWritten, Books.Title, BookAuthor.Priority, Authors.AuthorId, BookAuthor.AuthorId
--   FROM Authors INNER JOIN (Books INNER JOIN BookAuthor ON Books.BookId=BookAuthor.BookId)
--   ON Authors.AuthorId = BookAuthor.AuthorId
--   ORDER BY BookAuthor.Priority;
