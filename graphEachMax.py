#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import os
from pylab import *

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="blood", # your username
                      passwd="blood", # your password
                      db="BloodData") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("SELECT personID FROM BloodData.TestCount where count > 100 AND TestNameID = 55")

ids = cur.fetchall()

for person in ids :
    first = person[0]
    
    cur.execute("SELECT CollectDate, result FROM BloodData.Instance i JOIN BloodData.Test t ON t.InstanceID = i.ID WHERE PersonID = " + str(first) + " AND TestNameID = 55 Group By CollectDate order by PersonID, CollectDate")

    dates=[]
    results=[]

    for row in cur.fetchall() :
        dates.append(row[0])
        results.append(row[1])

        plt.scatter(dates, results)
        plt.gcf().autofmt_xdate()

        x = mdt.date2num(dates)

        (m,b) = polyfit(x, results,1)
        yp = polyval([m,b], x)
    plt.plot(dates, yp)

    directory = "/home/jared/DevTools/BloodData/graphs/" + str(first)

    if not os.path.exists(directory):
        os.makedirs(directory)
    print "created Directory: " + str(directory)
        
    plt.savefig(directory + "/HCTregression.png")
#    plt.show()
    plt.clf()
