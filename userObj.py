#User Object
class userObj:
    def __init__(self, username :str, password :str):
        self.username = username
        self.password = password
    loggedIn = False #Logged in Status, False == GUEST
    _id = -1
    billingId = None
    shippingId = None
    shippingAddreId = -1
    billingAddreID = -1
    basket = {} #Dic that stores {BookdId: quantity}
    shopping = True #flag to see if user is shoping (True) or checking out (False)