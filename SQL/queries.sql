-- Finds title, author, price from Books table, used in __main__.printBasket() to get information of all books in the user's basket
SELECT title, author, price, FROM Books WHERE id IN (%s);

-- Returns the sum sold books of a specific book_id, between a given date. Used in: __main__.orderBooks() to order books based off of how many of a given book was sold in the past 30 days
SELECT SUM(quantity) FROM Transactions WHERE date >= %s AND date < %s AND books_id = %s;

--Used in: __mian__.orderBooks() to add a book to the BooksToOrder table 
INSERT into BooksToOrder (books_id, quantity) VALUES (%s,%s) RETURNING books_id;

-- Finds the price and stock level of a given book, used in __main__.caclPrice() to (1)calculate the price of a book in the user's basket and (2) check if there is enough stock for the user to purchase
SELECT price, stock FROM Books WHERE id = %s;

-- Finds the stock of a given book. Used in __main__.updateStock() to find the current stock of a book
SELECT stock FROM Books where id = %s;

-- Updates the stock level of a Book after a user has purched a book. Used in __main__.updateStock()
UPDATE Books SET stock = %s WHERE id = %s RETURNING id;

-- Used in __main__.completeTransaction() to record a transaction by a customer
INSERT into Transactions (books_id, users_id, quantity, date, billing_id, shipping_id) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id;

-- Used in __main__.searchISBN() to search for information on a book that matches the given ISBN
SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE ISBN = %s;

-- Used in __main__.searchTitle to search for information on a book/ books that match the given title
SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE title = %s;

-- Used in __main__.searchGenre to search for information on all books of a given genre
SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE genre = %s;

-- Used in __main__.regsShippingInformation to add a new entry the ShippingInformation table
INSERT into ShippingInformation (address_id, name) VALUES (%s,%s) RETURNING id;

-- Used in __main__.regsBillingInfor() to add a new entry in the BillingInformation table
INSERT into BillingInformation (address_id, creditCardNum, name) VALUES (%s,%s,%s) RETURNING id;

-- Used in __main.regsAddress() to add a new entry to the Address table
INSERT into Address (streetNumber, streetName, zipPostalCode) VALUES (%s,%s,%s,%s) RETURNING id;

-- Used in __main__.register() to add a new entry to the Users table, two versions depending on if the user wants to assiciate billingShipping information to the account when they register
INSERT into Users (username, password, billing_id, shipping_id) VALUES (%s,%s,%s,%s) RETURNING id;
INSERT into Users (username, password) VALUES (%s,%s) RETURNING id;

-- Used in __main__.loggin() to check if the username and password given match any entries in the Users table
SELECT id, billing_id, shipping_id from Users WHERE username = %s AND password = %s;

-- ADMIN ---------------------------------------
-- Used in admin.salesEXP to find the revenue (price * quantity) of all books sold in the past 30 days
SELECT SUM(A.price * B.quantity) FROM Books as A, Transactions as B WHERE B.date >= %s AND B.date <= %s;

-- Used in admin.salesEXP to find the cost of books that need to be ordered in BooksToOrder table
SELECT SUM(A.price * B.quantity) FROM Books as A, BooksToOrder as B WHERE A.id = B.books_id;

-- Used in admin.SalesGenre to find the number of books sold from each genre
SELECT DISTINCT (A.genre), SUM (B.quantity) FROM books as A, Transactions as B WHERE A.id = B.books_id GROUP BY A.genre;

-- Used in admin.salesAuthor to find the number of books sold from each author
SELECT DISTINCT (A.author), SUM (B.quantity) FROM books as A, Transactions as B WHERE b.books_id = A.id GROUP BY A.author;

-- Used in admin.orderBook() to a book to the BooksToOrder table
INSERT into BooksToOrder (books_id, quantity) VALUES (%s,%s) RETURNING books_id;

-- Used in admin.searchByTitle to find information on a book based off the title
SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE title = %s;

-- Used in admin.searchByISBN() to find information on a book based off of the given ISBN
SELECT id from Books WHERE ISBN = %s;

-- Used in admin.regsAddres() to add an address to the Address table, used to add an address for a Publisher
INSERT into Address (streetNumber, streetName, zipPostalCode) VALUES (%s,%s,%s,%s) RETURNING id;

-- Used in admin.addNewPublisher() to add a new publisher to the Publisher table
INSERT into Publisher (name, address_id, emial, phoneNum, bankAcount) VALUES (%s,%s,%s,%s,%s) RETURNING id;

-- Used in admin.associatePublisher() to add a new entry to the Publishes table
INSERT into Publishes (publisherName, cost, book_ISBN, percentReturn) RETURNING publisherName;

-- Used in admin.addNewBook() to add a new book to the store
INSERT into Books (title, author, genre, numpages, isbn, price, stock) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;

-- Used in admin.loggin() to check if the username and password is in the Users table and that their user._id is in the OwnersAdmins table
SELECT id from Users WHERE username = %s AND password = %s and id in (SELECT user_id from ownersadmins);

