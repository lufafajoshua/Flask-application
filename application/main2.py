from flask import Flask, request, render_template, current_app,redirect, current_app
#from myapp import app
#from flask import current_app as app#or use "from myapp import app" incase of errors
from datetime import datetime 
from forms import MemberForm, SearchForm
from tables import Summary
from models import Member#This is the model with which we are going to pass our dat for storage in the database
import mysql.connector

#pass an application/request context object to access the objects outside the function
    # app_context = app.app_context()
    # app_context.push() 

class Dbconnect(object):
    def __init__(self):
        self.dbconnection = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            user = 'joshualufafa',
            passwd = 'yrueh6472wjdwj0m3',
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

@app.route('/summary')
def summary(): #creat a summary of the entire records in the database, eg tota l number of females, males        
    sql_query = ("SELECT *, COUNT(*) FROM member_data")#select all the data
    db2.dbcursor.execute(sql_query)
    results = db2.dbcursor.fetchall()
    for i in results:
        row1 = i[1]
        total_membership = i[28]#get the rows with which the summary of the data is to created
        #print("Total membership: ", row28) #this is the total number of
    sql_query1 = "SELECT gender, COUNT(gender) FROM member_data WHERE gender='female'"
    db2.dbcursor.execute(sql_query1)
    results = db2.dbcursor.fetchall()
    for i in results:
        row0 = i[0]
        female = i[1]#this constitutes the total number of females in the database
        #print(row0, row1)
    sql_query2 = "SELECT gender, COUNT(gender) FROM member_data WHERE gender='male'"
    db2.dbcursor.execute(sql_query2)
    results = db2.dbcursor.fetchall()
    for i in results:
        row0 = i[0]
        male = i[1]#this constitutes the total number of males in the database
        #print(row0, row1)
    sql_query3 = "SELECT m_status, COUNT(m_status) FROM member_data WHERE m_status='single'"
    db2.dbcursor.execute(sql_query3)
    results = db2.dbcursor.fetchall()
    for i in results:
        row0 = i[0]
        single = i[1]#this constitutes the total number of singles in the database
        #print(row0, row1)
    sql_query4 = "SELECT m_status, COUNT(m_status) FROM member_data WHERE m_status='married'"
    #sql_query5 = "SELECT gender,COUNT(gender) FROM member_data WHERE gender='female'" #just in case of another summary to make
    db2.dbcursor.execute(sql_query4)
    results = db2.dbcursor.fetchall()
    for i in results:
        row0 = i[0]
        married = i[1]#this constitutes the total number of married couples in the database
        #print(row0, row1)

    table = Summary(results)
    #result = {'Total_membership': total_membership, 'females': female, 'male': male, 'singles': single, 'married': married}    

    return render_template('summary.html', table=table)#pass the result object as a context to the summary.html page    

if __name__ == '__main__':
    app.run()
  