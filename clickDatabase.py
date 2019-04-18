#CS304 Project
#Dana, Erica, and Gabby

import sys
import MySQLdb

'''our clickdb connection'''
def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn
    

#put our functions here
   
if __name__ == '__main__':
    conn = getConn('clickdb')