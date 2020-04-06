-- Creating tables needed for the Look Inna Book Database
CREATE TABLE Address(
	id bigserial PRIMARY KEY,
	streetNumber INT NOT NULL CHECK (streetNumber > 0),
	streetName VARCHAR (100) NOT NULL,
	zipPostalCode VARCHAR (6) NOT NULL,
	aptComplexNum INT
)

CREATE TABLE BillingInformation(
	id bigserial PRIMARY KEY,
	address_id BIGINT REFERENCES Address(id),
	creditCardNum INT NOT NULL,
	name VARCHAR (100) NOT NULL
)

CREATE TABLE ShippingInformation(
	id bigserial PRIMARY KEY,
	address_id BIGINT REFERENCES Address(id),
	name VARCHAR (100) NOT NULL
)

CREATE TABLE Users(
	id bigserial PRIMARY KEY,
	username VARCHAR (100) NOT NULL UNIQUE,
	password VARCHAR (100) NOT NULL,
	billing_id BIGINT REFERENCES BillingInformation(id),
	shipping_id BIGINT REFERENCES ShippingInformation(id)
)

CREATE TABLE ownersAdmins(
	user_id BIGINT NOT NULL UNIQUE REFERENCES Users(id)
)

CREATE TABLE Publisher(
	name VARCHAR (100) NOT NULL UNIQUE PRIMARY KEY,
	address_id BIGINT NOT NULL REFERENCES Address(id),
	email VARCHAR (100),
	phoneNum VARCHAR (12),
	bankAcount VARCHAR (30) NOT NULL
)

CREATE TABLE Books(
	id bigserial PRIMARY KEY,
	title VARCHAR (100) DEFAULT 'titleless Book',
	author VARCHAR (100) DEFAULT 'Unknown Author',
	genre VARCHAR (100),
	numPages INT CHECK (numPages > 0),
	ISBN VARCHAR (20) NOT NULL UNIQUE,
	price NUMERIC (10,2) NOT NULL CHECK (price > 0),
	stock INT NOT NULL CHECK (stock > 0)
)

CREATE TABLE Publishes(
	publisherName VARCHAR (100) NOT NULL REFERENCES Publisher(name),
	cost NUMERIC (10,2) NOT NULL CHECK (cost > 0),
	book_ISBN VARCHAR (20) NOT NULL REFERENCES Books(ISBN),
	percentReturn NUMERIC (3,2) NOT NULL CHECK (percentReturn > 0)
)

CREATE TABLE BooksToOrder(
	books_id BIGINT NOT NULL REFERENCES Books(id),
	quantity INT NOT NULL CHECK (quantity > 0)
)

CREATE TABLE Transactions(
	id bigserial PRIMARY KEY,
	books_id BIGINT NOT NULL REFERENCES Books(id),
	users_id BIGINT NOT NULL REFERENCES Users(id),
	quantity INT NOT NULL CHECK (quantity > 0),
	trackingNum bigserial,
	date DATE NOT NULL,
	billing_id BIGINT NOT NULL REFERENCES BillingInformation(id),
	shipping_id BIGINT NOT NULL REFERENCES ShippingInformation(id),
	shippingCompName VARCHAR (100) DEFAULT 'Default Shipping Company'
)