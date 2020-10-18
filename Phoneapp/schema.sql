DROP TABLE IF EXISTS phones;

CREATE TABLE customer (
  customerId INTEGER PRIMARY KEY AUTOINCREMENT,
  customerName VARCHAR(1000),
  customerPhoneNumber VARCHAR(11)
);

CREATE INDEX idx_customer_customerPhoneNumber ON customer (customerPhoneNumber);