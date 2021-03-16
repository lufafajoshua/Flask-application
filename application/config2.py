import mysql.connector

class Dbconnect(object):
    def __init__(self):
        self.dbconnection = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            user = 'joshlufafa',
            passwd = 'fhdu23AJ8j3hmvbluf',
            database = 'kyambogo'

        )
        self.dbcursor = self.dbconnection.cursor()
       
     #save changes to the database   
    def commit_db(self):
        self.dbconnection.commit()

    def rollback(self):
        self.dbconnection.rollback()    

    def close_db(self):
        self.dbcursor.close()
        self.dbconnection.close()

db2 = Dbconnect()