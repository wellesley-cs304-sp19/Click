"""Search for Project with different criteria; this is for public use"""
#Gabby

import MySQLdb
import sys
from connection import getConn



def getAllProjects(conn):
    """Returns all projects in the database"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''Select name,minHours,pay,location from project''')
    return curs.fetchall()
 
def sortProectByMinHoursAscending(conn):
    """Returns all projects ordered by Min Hours Required Ascending"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select name,minHours,pay,location from project order by minHours asc''')
    return curs.fetchall()
    
def sortProectByPayDescending(conn):
    """Returns all projects ordered by Pay Descending"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select name,minHours,pay,location from project order by pay desc''')
    return curs.fetchall()

def sortProjectByLocation(conn):
    """Returns all projects ordered by location"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select name,minHours,pay,location from project order by location''')
    return curs.fetchall()
    
def getProjectLocation(conn,location):
    """Returns all projects of a specific location"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select name,minHours,pay,location from project where location = %s''',[location])
    return curs.fetchall()
    
def multipleFilters(conn,fil,sort):
    """Returns projects after filtering and sorting"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if(sort=="Min Hours Ascending"):
        curs.execute('''select name,minHours,pay,location from project where location= %s order by minHours asc''',[fil])
    elif(sort=="Pay Descending"):
        curs.execute('''select name,minHours,pay,location from project where location= %s order by pay desc''',[fil])
    elif(sort=="Alphabetical By Location"):
        curs.execute('''select name,minHours,pay,location from project where location= %s order by location''',[fil])
        
if __name__ == '__main__':
    conn=getConn()