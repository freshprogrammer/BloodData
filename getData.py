#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import sys
import matplotlib.pyplot as plt
import os

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="blood", # your username
                      passwd="blood", # your password
                      db="BloodData") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("SELECT DISTINCT PersonID FROM BloodData.Instance;")

ids = cur.fetchall()

#first = ids[0][0]


for person in ids :
    first = person[0]
    
    response = raw_input("go Again? (y/n) ")
    if response == "y":
        print "person: " + str(first)
    else:
        break;

    

    directory = "/home/jared/DevTools/bloodData/graphs/" + str(first) + "/"

    if not os.path.exists(directory):
        os.makedirs(directory)
        print "created Directory: " + str(directory)
    
    
    cur.execute("SELECT DISTINCT t.TestNameID FROM BloodData.Instance i JOIN BloodData.Test t ON t.InstanceID = i.ID WHERE i.PersonID = " + str(first))

    tests = cur.fetchall()

    for test in tests :
        query = "SELECT DISTINCT `Name` FROM TestName WHERE ID = " + str(test[0])
        cur.execute(query)
        testName = cur.fetchone()[0]
        print "Results for test: " + str(testName)

    
        cur.execute("SELECT Distinct runDate, result FROM BloodData.Instance i JOIN BloodData.Test t ON t.InstanceID = i.ID WHERE i.PersonID = " + str(first) + " AND t.TestNameID = " + str(test[0]) + " GROUP BY runDate ORDER BY runDate")

        dates=[]
        results=[]
    
        for row in cur.fetchall() :
            dates.append(row[0])
            results.append(row[1])

        plt.plot(dates, results)
        plt.gcf().autofmt_xdate()

        pic = directory + str(testName) + ".png"
        
        plt.savefig(pic)
        plt.clf()

        print 'wrote graph to "' + pic + '"'
        
#        plt.show()



    

# print all the first cell of all the rows
#for row in ids :
#    cur.execute("SELECT * FROM BloodData.Instance i JOIN BloodData.Test t ON t.InstanceID = i.ID WHERE i.PersonID = " + str(row[0]))
    
#    for row2 in cur.fetchall() :
#        for item in row2 :
#            sys.stdout.write(str(item) + ", ")
#        print "\n"

