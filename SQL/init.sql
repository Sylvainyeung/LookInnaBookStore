INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Earth BBC', 'David', 'Nature', '432', '333432', '99.90', 30);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Harry Potter', 'JKR', 'Magic', '300', '123345', '20.33', 10);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Harry Potter', 'JKR FAKER', 'Magic', '300', '1253345', '20.33', 10); 
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Midnight in Chernobyl', 'Adam Higginbotham', 'History', '300', '9781501134616', '18.39', 30);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('The Nickel Boys', 'Colson Whitehead', 'History', '130', '9780385537070', '12.48', 12);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('The Things We Cannot Say', 'Kelly Rimmer', 'History', '448', '9781525823565', '21.77', 34);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Life of Pi', 'Yann Martel', 'Classics', '460', '9780156027328', '5.99', 23);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('The Catcher in the Rye', 'J.D. Salinger', 'Classics', '277', '9780316450867', '12.49', 10);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Rot & Ruin', 'Jonathan Maberry', 'Horror', '458', '9781442402331', '14.89', 16);
INSERT into Books (title, author, genre, numpages, ISBN, price, stock) VALUES ('Feed', 'Mira Grant', 'Horror', '458', '9780316081054', '11.49', 14);

INSERT INTO address (streetNumber, streetName, zipPostalCode) VALUES (100, 'AnyHw', '1234') RETURNING id;
INSERT INTO address (streetNumber, streetName, zipPostalCode) VALUES (123, 'Here Str.', '4321') RETURNING id;

INSERT into Publisher (name, address_id, email, phoneNum, bankAcount) VALUES ('Bird Pub. Inc.', 1,'fakeEmail@google.ca', '123-1234', 'AC123');
INSERT into Publisher (name, address_id, email, phoneNum, bankAcount) VALUES ('Woof Pub. Inc.', 2,'BarkWoof@Dog.ca', '001-0001', 'Woof1');

INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Bird Pub. Inc.', 23.20, 333432, 0.34);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Bird Pub. Inc.', 3.00, 123345, 0.24);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Bird Pub. Inc.', 4.21, 1253345, 0.01);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Bird Pub. Inc.', 1.00, 9781501134616, 0.5);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Woof Pub. Inc.', 2.00, 9780385537070, 0.4);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Woof Pub. Inc.', 2.00, 9781525823565, 0.12);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Woof Pub. Inc.', 3.00, 9780156027328, 0.1);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Woof Pub. Inc.', 3.00, 9780316450867, 0.3);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Woof Pub. Inc.', 4.00, 9781442402331, 0.23);
INSERT INTO Publishes (publisherName, cost, book_ISBN, percentReturn) VALUES ('Woof Pub. Inc.', 4.00, 9780316081054, 0.34);

INSERT INTO address (streetNumber, streetName, zipPostalCode) VALUES (101, 'Bin', '1001') RETURNING id;
INSERT INTO ShippingInformation (address_id, name) VALUES (3, 'Joe');
INSERT INTO BillingInformation (address_id, creditCardNum, name) VALUES (3, '0101010', 'Joe');
INSERT INTO Users (username, password, billing_id, shipping_id) VALUES ('user1', 'user1', 1 ,1);
INSERT INTO ownserAdmin (user_id) VALUES (1);

INSERT INTO Users (username, password) VALUES ('user2', 'user2');

INSERT INTO BooksToOrder (books_id, quantity) VALUES (1, 10);
