import userObj as userObj
import admin as admin
import database as db

import os
import sys
import datetime


clear = lambda: os.system('cls') #clear the screen

BOOKATTRIBUTES = ['Title', 'Author', 'Genre', 'Number of Pages', 'ISBN','Price', 'Stock']
ATTRIBUTEINDEX = [1,2,3,4,5,6,7]

CMD = -1

#HELPER FUNCTIONS-------------------------------------------------------------------------------------------------------#
#PRINTBASKET
def printBasket(database :db.databaseObj, Userbasket :dict):
    print("Your basket contains: ")

    sqlString = 'SELECT title, author, price, FROM Books WHERE id IN (%s)'
    basket = tuple(Userbasket.keys())
    args = (basket,)
    result = database.query(sqlString, args)

    printBooks(result, ['title', 'author', 'price',], [0,1,2], len(result))
    return

#PRINTBOOK#
#PRINTBOOK#
#Prints the information of the book
#PARAMS:
# books: list of book results return from SQL query 
# catag: list of catagories/ book attributes to display 
# indexList: of containing the indicies of the attributes of the SQL query
# size: length of the books.list
def printBooks(books :list, catag :list, indexList :list, size :int):
    for i in range (0, size): #loops through the list of books
        print ('Book: '+ str(i+1))
        for x in indexList:
            print(catag[indexList.index(x)] + ": " + str(books[i][x]))
    return

#Error checking for user input. Used to print a prompt, and checks if the user input is in the correct range and can be converted to an int
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

#-------------------------------------------------------------------------------------------------------------------#

#ORDERBOOKS#
#orders more books based of sale from last month
def orderBooks(database :db.databaseObj, bookId :int):
    today = datetime.date.today()
    prevMonth = today - datetime.timedelta(days = 30) #subtract 1 month from current date

    #Find amount of bookId purchased over the last month
    sqlString = 'SELECT SUM(quantity) FROM Transactions WHERE date >= %s AND date < %s AND books_id = %s;'
    args = (prevMonth, today, bookId)
    result = database.query(sqlString, args)

    quantity = result[0][0]
    sqlString = 'INSERT into BooksToOrder (books_id, quantity) VALUES (%s,%s) RETURNING books_id;'
    args = (bookId, quantity)
    database.query(sqlString, args)

    #TODO: Send email to Publisher
    return

#PURCHASEBOOK--------------------------------------------------------------------------------------------------------------------#
#adds {bookID: quantity} to user's basket
def purchaseBook(database :db.databaseObj, user :userObj.userObj, bookId :int, title :str, stock:int):
    print("stock = {}".format(stock))
    quantity = printPrmtINT('How many copies of {}, do you want?\n(0)-To go back\nEnter Choice: '.format(title), stock)
    if quantity == 0: return;

    #adds {bookId: quantity} to the user's basket. If the bookID-key is already in the basket, increase the value instead
    user.basket[bookId] = user.basket.get(bookId, 0)+quantity 

    return
#------------------------------------------------------------------------------------------------------------------------------#

#CHECKOUT--------------------------------------------------------------------------------------------------------------------#
#loops through loops in user's basket, caclulates the total price and completes the transaction
def checkOut(database :db.databaseObj, user :userObj.userObj)->float:
    printBasket(database, user.basket);
    total = 0
    #Loop through all books in the bakset and calculates the total price
    for bookId, quantity in user.basket.items(): 
        subtotal = calcPrice (database, user, bookId, quantity)
        total = total + subtotal
    print('You\'re total is: {}'.format(total))
    
    completeTransaction(database, user)
    return total


#CALCPRICE#
#Returns the price a book times the number of copies perchased
def calcPrice(database :db.databaseObj, user :userObj.userObj, bookId :int, qauntity :int)->float:
    sqlString = 'SELECT price, stock FROM Books WHERE id = %s;'
    args = (bookId,)
    result= database.query(sqlString, args)
    price = result[0][0]
    stock = result[0][1]

    if qauntity > stock:
        print("Not enough inventory to purchase that many books, you may have {}".format(stock))
        subTotal = price * stock
        user.basket[bookId] = stock
    else:
        subTotal = price * qauntity
    return subTotal

#UPDATESTOCK
#Updates the stock information in the Books table after user has purchased them
def updateStock(database :db.databaseObj, user :userObj.userObj):
    for bookID, quantity in user.basket.items():
        sqlString = 'SELECT stock FROM Books where id = %s;'
        args = (bookID,)
        result = database.query(sqlString, args)
        oldStock = result[0][0]
        newStock = oldStock - quantity
        sqlString = 'UPDATE Books SET stock = %s WHERE id = %s RETURNING id;'
        args= (newStock, bookID)
        database.query(sqlString, args)
        if newStock < 3: #if inventory drops below 3 -> order more books
            orderBooks(database, bookID)
    return

#COMPLETETRANSCATION#
def completeTransaction(database :db.databaseObj, user :userObj.userObj):
    if user.loggedIn == False: #if viewing as GUEST
        CMD = printPrmtINT('you need to log in before making a purchase.\nDo you want to:\n(1)-loggin\n(2)-regiser an account?\n Enter choice: ', 2)
        if CMD == 1:
            loggin(database, user)
        else:
            register(database, user)

    if user.billingId == None and user.shippingId == None: #if user doesn't have registered billing and shipping information
        setUpBillingshippingInfo(database, user)

    today = datetime.date.today() #get today's date

    for bookId, quantity in user.basket.items():
        sqlString = 'INSERT into Transactions (books_id, users_id, quantity, date, billing_id, shipping_id) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id;'
        args = (bookId, user._id, quantity, today, user.billingId, user.shippingId)
        database.query(sqlString, args)

    updateStock(database, user)
    print("Thank you for shopping at Look Inna Book Store")
    return


#SEARCH dispatcher--------------------------------------------------------------------------------------------------------------------#
def search(database :db.databaseObj, user :userObj.userObj)->list:
    clear()
    CMD = printPrmtINT('Do you want to search by:\n(1)-ISBN\n(2)-Title?\nEnter Choice: ',2)
    if CMD == 1:
        result = searchISBN(database)
    else:
        result = searchTitle(database)

    return result

#SEARCHISBN#
#Search for single book by ISBN
def searchISBN(database :db.databaseObj)->list:
    ISBN = input('What is the ISBN of the book you are looking for?: ')

    sqlString = 'SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE ISBN = %s;'
    args = (ISBN,)
    result = database.query(sqlString, args)

    return result

#SEARCHTITLE#
#Search for book by title, can return multiple books sharing the same title
def searchTitle(database :db.databaseObj)->list:
    title = input('What is the title of the book you are looking for?: ')

    sqlString = 'SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE title = %s;'
    args = (title,)
    result = database.query(sqlString, args)

    return result
#---------------------------------------------------------------------------------------------------------------------------------#

#BROWSE Dispatcher-----------------------------------------------------------------------------------------------------------------#
def browse(database :db.databaseObj, user :userObj.userObj)->list:
    clear()
    CMD = printPrmtINT('Do you want to browse by:\n(1)-Genre?\n(2)-Author?\nEnter choice: ', 2)
    if CMD == 1:
        result = browseGenre(database)
    else:
        result = searchAuthor(database)

    return result

#BROWSEGENRE#
def browseGenre(database :db.databaseObj)->list:
    sqlString = 'SELECT DISTINCT genre from Books;'
    result = database.query(sqlString, None)
    clear()

    #prints all the genres found
    print('Avaliable genres:')
    for x in result[0]:
        print('('+str(result[0].index(x)+1)+')' + "-" + str(x))
    CMD = printPrmtINT('which genre do you want to see?\nEnter Choice: ',len(result[0]))
    if CMD == 0:
        return None
    else:
        result = searchGenre(database, str(result[0][CMD-1]))
    return result

#SEARCHGENRE#
def searchGenre(database :db.databaseObj, genre :str) ->list:
    sqlString = 'SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE genre = %s;'
    args = (genre,)
    result = database.query(sqlString,args)
    return result

#SEARCHAUTHOR#
def searchAuthor(database :db.databaseObj)->list:
    author = input("Name of author to search for: ")

    sqlString = 'SELECT id, title, author, genre, numPages, ISBN, price, stock FROM Books WHERE author = %s;'
    args = (author,)
    result = database.query(sqlString,args)
    return result

#---------------------------------------------------------------------------------------------------------------------------------#

#Inserting into ShippingInformation Table -----------------------------------------------------------------------------------------#
def regsShippingInfo(database :db.databaseObj, user :userObj.userObj, addressId :int)->int:
    name = input("Name for shipping address: ")

    sqlString = 'INSERT into ShippingInformation (address_id, name) VALUES (%s,%s) RETURNING id;'
    args= (addressId, name)
    result = database.query(sqlString, args)
    if result[0] == -1:
        print('Error in registering Shipping info.')
        shippingId = regsShippingInfo(database, user, addressId)
        
    shippingId = result[0][0]
    return shippingId

#Inserting into the BillingInformation Table
def regsBillingInfo(database :db.databaseObj, user :userObj.userObj, addressId :int)->int:
    ccNumb = input("Input your credit card namber: ")
    name = input("Name on credit card: ")

    sqlString = 'INSERT into BillingInformation (address_id, creditCardNum, name) VALUES (%s,%s,%s) RETURNING id;'
    args = (addressId, ccNumb, name)
    result = database.query(sqlString, args)
    if result[0] == -1:
        print('Error in registering billing info.')
        billingId = regsBillingInfo(database, user, addressId)
        
    billingId = result[0][0]
    return billingId

#REGSADDRESS#
#registering an entry into the Addresss table
def regsAddress(database :db.databaseObj, user :userObj.userObj,)->int:
    streetNumber = input("Enter your street Number: ")
    streetName = input("Enter the name of your street: ")
    zipPostal = input("Enter your ZIP/Postal code: ")
    aptNum = input("Enter your apartment complex number, leave blank if not applicable: ")

    sqlString = 'INSERT into Address (streetNumber, streetName, zipPostalCode) VALUES (%s,%s,%s,%s) RETURNING id;'
    args = (streetNumber, streetName, zipPostal, aptNum)
    result = database.query(sqlString, args)
    if result[0] == -1:
        print('Error in registering address.')
        addressId = regsAddress(database, user)

    addressId = result[0][0]
    return addressId

#SETUPBILLINGSHIPPINGINFO
def setUpBillingshippingInfo(database :db.databaseObj, user :userObj.userObj):
    clear()
    print("Please enter information for your Billing Address")
    billingAddreID = regsAddress(database, user) #Creating an Address for billing Info
    user.billingAddreID = billingAddreID
    billingId = regsBillingInfo(database, user, billingAddreID) #making the billing info
    user.billingId = billingId

    CMD = printPrmtINT('Do you want to enter a billing and shipping address now?\n(1)-Yes\n(2)-No\nEnter choice: ', 2)

    #Selecting the shiping Address ID
    if CMD == 1:
        shippingAddreId = user.billingAddreID #Using the same address for billing and shipping information
    else: 
        clear()
        print("Please enter information for your Shipping Address")
        shippingAddreId = regsAddress(database, user)#making a new address for the shipping information

    #Making/ inserting an entry for shipping info
    user.shippingAddreId = shippingAddreId
    shippingId = regsShippingInfo(database, user, shippingAddreId) #making the shipping Address
    user.shippingId = shippingId
    
    return
#---------------------------------------------------------------------------------------------------------------------------------#

#MENU#
def menu(database :db.databaseObj, user: userObj.userObj):
    clear()
    print('Hello, {}'.format(user.username))

    while user.shopping:#Main store loop
        CMD = printPrmtINT('Do you want to:\n(1)-Search for a specific book?\n(2)-Browse\nEnter choice: ', 2)
        if CMD == 0: user.shopping = False; break; #Finished shopping
        
        if CMD == 1:
            result = search(database, user) #Search dispatcher
        else:
            result = browse(database, user) #Browse dispatcher

        if result == None:
            print("There were no book found by that criteria")
        else:
            clear()
            printBooks(result, BOOKATTRIBUTES, ATTRIBUTEINDEX, len(result)) #prints the information of all the books found

            CMD = printPrmtINT('Do you want to purchace any of these books?\nEnter the Book number you want.\n(0)- if you do not want any\nEnter Choice: ', len(result))
            if CMD != 0:
                purchaseBook(database, user, result[CMD-1][0], result[CMD-1][1], result[CMD-1][7]) #Adds book to User's basket
                
        CMD = printPrmtINT('Do you want to:\n(1)-Continue shopping?\n(2)-Go to checkout?\nEnter choice: ', 2)
        if CMD == 2:
            #Go to CheckOut and leave the store after
            checkOut(database, user)
            user.shopping = False
            break
        clear()
        
    database.disconnect() #Leave the store
    
    return
#---------------------------------------------------------------------------------------------------------------------------------#
#Registering a new user 
#REGISER#
def register(database :db.databaseObj, user :userObj.userObj):
    clear()
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    user.username = username
    user.password = password
    CMD = printPrmtINT('Do you want to enter a billing and shipping address now?\n(1)-Yes\n(2)-No\nEnter choice: ', 2)
    
    if CMD == 1: #Make a new user with Billing and Shipping address, first making an address
        setUpBillingshippingInfo(database, user)

        #Inserting the new User
        sqlString = 'INSERT into Users (username, password, billing_id, shipping_id) VALUES (%s,%s,%s,%s) RETURNING id;'
        args = (username, password, user.billingId, user.shippingId)

    else: #Make a new user without a billing and shipping address
        sqlString = 'INSERT into Users (username, password) VALUES (%s,%s) RETURNING id;'
        args = (username, password)

    userId = (database.query(sqlString, args))[0][0]
    user._id = userId
    user.loggedIn = True
    return

def loggin(database :db.databaseObj, user :userObj.userObj)->list:
    clear()
    #Setting up Users Query-> if user is in database query will return id of user, else return None
    username = input("Enter username: ")
    password = input("Enter password: ")
    user.username = username
    sqlString = 'SELECT id, billing_id, shipping_id from Users WHERE username = %s AND password = %s;'
    args = (username, password)
    result = database.query(sqlString, args)

    if result == None: #Could not login
        input("Incorrect Username or Password, Press 'Enter' to try again.")
        result = loggin(database, user)

   #Logged in Successfully, setting user's parameters
    user.loggedIn = True
    user._id = result[0][0]
    user.billingId = result[0][1]
    user.shippingId = result[0][2]
    return result
    
#---------------------------------------------------------------------------------------------------------------------------------#
def main():
    clear()
    database = db.databaseObj() #Create Database object and connect
    user = userObj.userObj("","")

    CMD = printPrmtINT("Do you have an account?\n(1)-Yes \n(2)-No, Register? \n(3)-No, Continue as Guest\n(0)-if you are the owner/admin\nEnter choice: ", 3)
    if CMD == 0:
        admin.adminLoggin(database) #admin loggin
    elif CMD == 1:
        loggin(database, user) #user loggin
    elif CMD == 2:
        register(database, user) #registering a new user
    elif CMD == 3:
        user = userObj.userObj("Guest","") #GUEST account
    
    menu(database, user)

    print("Should not get here")
    database.disconnect()
    sys.exit(-1)
        
    return

if __name__ == "__main__":
    main()