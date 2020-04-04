import database as db
import os
import datetime

#Admin Object
class adminObj(object):
    def __init__(self, username :str, password :str):
        self.username = username
        self.password = password
    adminId = -1
    loggedIn = False

clear = lambda: os.system('cls') #clear the screen

CMD = -1
BOOKATTRIBUTES = ['Title', 'Author', 'Genre', 'Number of Pages', 'ISBN','Price', 'Stock']
ATTRIBUTEINDEX = [1,2,3,4,5,6,7]

#HELPER FUNCTIONS-------------------------------------------------------------------------------------------------------#
#PRINTBOOK#
def printBooks(books :tuple, catag :list, index :list, size :int):
    for i in range (0, size):
        print ('Book: '+ str(i+1))
        for x in index:
            print(catag[index.index(x)] + ": " + str(books[i][x]))
    return

#Error checking for user input
def printPrmtINT(question :str, maxVal : int)->int:
    userInput = input(question)
    try:
        int(userInput)
    except:
        print("Invalid Input")
        userInput = printPrmtINT(question, maxVal)

    if int(userInput) > maxVal:
        print("Invalid Input")
        userInput = printPrmtINT(question, maxVal)
    return int(userInput)
#-----------------------------------------------------------------------------------------------------------------#
#VIEWREPORTS#--------------------------------------------------------------------------------------------------------------#
#Reports Dispatcher
def viewReports(database :db.databaseObj):
    clear()
    CMD = printPrmtINT('Do you want to see:\n(1)-Sales vs Expenditures?\n(2)-Sales by genre?\n(3)-Sales per author?\nEnter choice: ', 3)
    if CMD == 1:
        salesEXP(database) #Sales vs Expenditures
        return
    elif CMD == 2:
        salesGenre(database) #Sales by Genre
        return
    elif CMD == 3:
        salesAuthor(database) #Salse by Author
        return
    return

#Sales vs Expenditures
def salesEXP(database :db.databaseObj):
    today = datetime.date.today()
    prevMonth = today - datetime.timedelta(days = 30) #subtract 1 month from current date

    #finds the total revenu from Transaction.bookd_id, Transaction.quantity Books.price of all books sold in the last month
    sqlString = 'SELECT SUM(A.price * B.quantity) FROM Books as A, Transactions as B WHERE B.date >= %s AND B.date <= %s;'
    args = (prevMonth, today)
    result = database.query(sqlString, args)
    salesTotal = result[0][0]

    print("Total Revenue from the last 30 days ={}".format(salesTotal))

    sqlString = 'SELECT SUM(A.price * B.quantity) FROM Books as A, BooksToOrder as B WHERE A.id = B.books_id;'
    args = ()
    result = database.query(sqlString, args)

    expenTotal = result[0][0]

    print("Total expenditure from Books-to-order = {}".format(expenTotal))
    return

#Sales by Genre
def salesGenre(database :db.databaseObj):
    sqlString = 'SELECT DISTINCT (A.genre), SUM (B.quantity) FROM books as A, Transactions as B WHERE A.id = B.books_id GROUP BY A.genre;'
    args = ()
    result = database.query(sqlString, args)
    clear()
    print('SALES BY GENRE:')
    for x in result:
        print("{} = {}(books sold)".format(x[0], x[1]))
    return

#Salse by Author
def salesAuthor(database :db.databaseObj):
    sqlString = 'SELECT DISTINCT (A.author), SUM (B.quantity) FROM books as A, Transactions as B WHERE b.books_id = A.id GROUP BY A.author;'
    args = ()
    result = database.query(sqlString, args)
    clear()
    print('SALES BY AUTHOR:')
    for x in result:
        print("{} = {} (books sold)".format(x[0], x[1]))
    return

#------------------------------------------------------------------------------------------------------------------------#
#Adds an existing book to BooksToOrder table
def orderBook(database :db.databaseObj):
    clear()
    CMD = printPrmtINT('Do you want find the book you want to add by:\n(1)-ISBN\n(2)-Title\n(3)-order a brand new Book\nEnter choice: ', 3)
    if CMD == 1:
        bookId = searchByISBN(database)
    elif CMD == 2:
        bookId = searchByTitle(database)
    elif CMD == 3:
        bookdId = addNewBook(database)
    else:
        return
    
    quantity = printPrmtINT('How many copies do you want to order?: ',99999)

    sqlString = 'INSERT into BooksToOrder (books_id, quantity) VALUES (%s,%s) RETURNING books_id;'
    args = (bookId, quantity)
    database.query(sqlString, args)
    return

#searches for the book based off of title
def searchByTitle(database :db.databaseObj)->int:
    title = input('What is the title of the book you are looking for?: ')

    sqlString = 'SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE title = %s;'
    args = (title,)
    result = database.query(sqlString, args)

    printBooks(result, BOOKATTRIBUTES, ATTRIBUTEINDEX, len(result))
    CMD = printPrmtINT('Which of these books do you want to order?\nEnter the Book number you want.\n(0)- if you do not want any\nEnter Choice: ', len(result))
    if CMD == 0:
        return
    else:
        bookId = result[CMD-1][0]
    return bookId

#Finds bookID using ISBN number
def searchByISBN(database :db.databaseObj)->int:
    ISBN = input('What is the ISBN number of the book you want to order?: ')
    
    sqlString = 'SELECT id from Books WHERE ISBN = %s;'
    args = (ISBN,)
    result = database.query(sqlString, args)
    bookId = result[0][0]

    return bookId

#----------------------------------------------------------------------------------------------------------------------------------------#
#adds an address for the publisher
def regsAddress(database :db.databaseObj)->int:
    print('Enter Publisher\'s address information')
    streetNumber = input("Enter street number: ")
    streetName = input("Enter street name: ")
    zipPostal = input("Enter ZIP/Postal code: ")
    aptNum = input("Enter apartment complex number, leave blank if not applicable: ")

    sqlString = 'INSERT into Address (streetNumber, streetName, zipPostalCode) VALUES (%s,%s,%s,%s) RETURNING id;'
    args = (streetNumber, streetName, zipPostal, aptNum)
    result = database.query(sqlString, args)
    addressId = result[0][0]
   
    return addressId

#adds a new publisher
def addNewPublisher(database :db.databaseObj):
    clear()
    print("Please input the information for the new publisher")
    pubName = input('Publisher name: ')
    email = input('Publisher e-mail: ')
    phone = input('Publisher phone number: ')
    bankAccount = input('Publisher bank accnout number: ')
    addressID = regsAddress(database)

    sqlString = 'INSERT into Publisher (name, address_id, emial, phoneNum, bankAcount) VALUES (%s,%s,%s,%s,%s) RETURNING id;'
    args = (pubName, addressID, email, phone, bankAccount)
    database.query(sqlString, args)
    return

#inserts into the Publishes table
#assiciates a publisher to a Book
def associatePublisher(database :db.databaseObj, ISBN :str):
    pubName = input('Who is the publisher of the book?: ')
    cost = input('How much does the book cost to buy from the publisher?: ')
    percentReturn = input ('What percent of the sale price is returned to the publisher?: ')

    sqlString = 'INSERT into Publishes (publisherName, cost, book_ISBN, percentReturn) RETURNING publisherName;'
    args = (pubName, cost, ISBN, percentReturn)
    result = database.query(sqlString, args)
    if result == None: #if adims tries to associate a book with a publisher that is not in the publisher table
        print("That Publisher is not in the database, you need to add an entry for the publisher first")
        addNewPublisher(database) #add the publisher
        associatePublisher #then associate the new book with the new publisher 

    return

#adds a new book to the table
def addNewBook(database :db.databaseObj)->int:
    clear()
    title = input('Enter Book title: ')
    author = input('Enter book author: ')
    genre = input('Enter book genre: ')
    numPages = input('Enter number of pages for the book: ')
    ISBN = input('Enter ISBN of the book: ')
    price = input('Enter price for the book: ')
    stock = input('Enter amount of inventory: ')

    sqlString = 'INSERT into Books (title, author, genre, numpages, isbn, price, stock) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;'
    args = (title, author, genre, numPages, ISBN, price, stock)
    result = database.query(sqlString, args)

    bookID = result[0][0]

    associatePublisher(database, ISBN)
    return bookID

def menu(database :db.databaseObj, admin :adminObj):
    print('Hello, {}'.format(admin.username))
    while admin.loggedIn == True:
        CMD = printPrmtINT('Do you want to:\n(1)-Add a new book?\n(2)-Add a new Publisher\n(3)-Order a book?\n(4)-View reports\n(0)-To loggout\nEnter choice:', 4)
        
        if CMD == 1:
            addNewBook(database)
        elif CMD == 2:
            addNewPublisher(database)
        elif CMD == 3:
            orderBook(database)
        elif CMD == 4:
            viewReports(database)
        elif CMD == 0:
            database.disconnect()

    return

def adminLoggin(database :db.databaseObj):
    clear()
    result = None
    while result == None:
        adminUsername = input("Enter Admin username: ")
        adminPassword = input("Enter Admin password: ")
        sqlString = 'SELECT id from Users WHERE username = %s AND password = %s and id in (SELECT user_id from ownersadmins);'
        args = (adminUsername, adminPassword)
        result = database.query(sqlString, args)
        if result !=None: break;
        print('Incorrect admin username and password')
        input('Press Enter to try again')
        clear()
    
    #setting up Admin Object
    admin = adminObj(adminUsername, adminPassword)
    adminID = result[0][0]
    admin.adminId = adminID
    admin.loggedIn = True
    menu(database, admin)
    
    database.disconnect()
    return