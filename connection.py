#Gabby
import MySQLdb

'''our clickdb connection'''
def getConn(db='c9'):
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn