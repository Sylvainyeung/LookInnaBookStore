import psycopg2 as psycopg2
import sys

HOST = "localhost"
DATABASE = "Look Inna Book"
USER = "postgres"
PASSWORD = "winter"

class databaseObj():
    def __init__(self):
        try:
            self.con = psycopg2.connect(
                host = HOST,
                database = DATABASE,
                user = USER,
                password = PASSWORD)
            self.cursor = self.con.cursor()
            print("Connected to DB")
        except psycopg2.OperationalError as err:
            print("Could Not connect!! Error:")
            print(err)
            sys.exit(-1)

    def disconnect(self):
        print("Exiting the bookstore \n Good Bye...")
        self.cursor.close()
        self.con.close()
        sys.exit(0)

    #Sucessful queries return list of results, failed querries return -1
    def query(self, queryString :str, args :tuple):
        try:
            self.cursor.execute(queryString, args)
            self.con.commit()
            result = self.cursor.fetchall()
            if result == []: #If query result is empty
                return None
            else: #if query result is not empty
                return result
        except psycopg2.DatabaseError as err: #Failed query
            print (err)
            return [-1]
