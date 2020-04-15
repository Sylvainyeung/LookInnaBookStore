-- updates the stock after a transaction was made
CREATE Trigger updateStock AFTER INSERT on Transactions
REFERENCING new row as nrow
BEGIN atomic
	UPDATE Books
	SET stock = stock nrow.quantity
	WHERE id = nrow.books_id;
end;

-- Adds book to Books-to-Order table if stock becomes lower than 5
CREATE Trigger orderBooks AFTER Update on Books
REFERENCING new row as nrow
BEGIN atomic
	IF (nrow.stock < 5) THEN
	INSERT into BooksToOrder (books_id, quantity)
	VALUES (nrow.id, 5);
	END IF
end;