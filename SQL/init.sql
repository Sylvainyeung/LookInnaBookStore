INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Earth BBC', 'David', 'Nature', '432', '333432', '99.90', 30);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Harry Potter', 'JKR', 'Magic', '300', '123345', '20.33', 10);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Harry Potter', 'JKR FAKER', 'Magic', '300', '1253345', '20.33', 10);

INSERT INTO address (streetNumber, streetName, zipPostalCode) VALUES (100, 'AnyHw', '1234') RETURNING id;

INSERT into Publisher (name, address_id, email, phoneNum, bankAcount) VALUES ('Bird Pub. Inc.', 3,'fakeEmail@google.ca', '123-1234', 'AC123')

INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Bird Pub. Inc.', 23.20, 333432, 0.34);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Bird Pub. Inc.', 3.00, 123345, 0.24);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Bird Pub. Inc.', 4.21, 1253345, 0.01);
