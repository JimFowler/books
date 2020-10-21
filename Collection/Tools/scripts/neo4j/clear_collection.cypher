  //
  // Clear the constraints, nodes, and relationships from the database
  //
  
  DROP CONSTRAINT UniqueBusinessKey IF EXISTS;  
  DROP CONSTRAINT UniqueProjectKey IF EXISTS;
  DROP CONSTRAINT UniquePersonKey IF EXISTS;
  DROP CONSTRAINT UniqueBookKey IF EXISTS;
  DROP CONSTRAINT UniqueBookIdConstraint IF EXISTS;
  DROP CONSTRAINT UniqueBookAccessionConstraint IF EXISTS;

MATCH (b:Business) DETACH DELETE b;
MATCH (p:Project) DETACH DELETE p;
MATCH (p:Person) DETACH DELETE p;
MATCH (b:Book) DETACH DELETE b;
