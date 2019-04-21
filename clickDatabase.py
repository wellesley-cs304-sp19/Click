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

#gets student's profile from database
def getStudent(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''Select * from user where email = %s''', [email])
    return curs.fetchone()

#get all student's skills from database    
def studentSkills(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    #use inner join to get list of skills
    curs.execute('''select skill from skills inner join hasSkill using (sid)
    where hasSkill.email = %s''', [email])
    return curs.fetchall()
  
#removes skill from student  
def removeSkill(conn, email, skill):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''Select sid from skills where skill = %s''', [skill])
    skillNum = curs.fetchone().values()[0]
    nr = curs.execute('''delete from hasSkill where sid = %s and email = %s''', [skillNum, email])
    return nr

#adds skill to student    
def addSkill(conn, email, skill):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute('''Select sid from skills where skill = %s''', [skill])
    skillNum = curs.fetchone()
    #if skill not in skills table, add it
    if skillNum == None:
        curs.execute('''insert into skills(skill) values (%s)''', [skill])
        curs.execute('''Select sid from skills where skill = %s''', [skill])
        skillNum = curs.fetchone()
    #continue with inserting email and skill into hasSkill table
    nr = curs.execute('''insert into hasSkill(email, sid) values (%s, %s)''', [email, skillNum.values()[0]])
    return nr
    
#put rest of our functions here


#get info about a posting 
def getPosting(conn, pid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''Select * from project where pid = %s''', [pid])
    return curs.fetchone()
   
#SQL query to get pid, name, pay, minimum hours, location from project table using the pid    
def search_posting_pid(conn, pid): 
    curs = conn.cursor()
    curs.execute('''select pid,name,pay,minHours,
    location from project where pid = %s;''',
                    [pid])
    return curs.fetchone()  

#SQL code to insert posting using pid, name, pay, minimum hours, location    
def insert_posting(conn, pid, name, pay, minHours, location): 
    curs = conn.cursor()
    curs.execute('''insert into posting(pid,name,minHours, location)
values (%s,%s,%s, %s);''',
                    [pid,name,minHours,location])
    return curs
  
#SQL query to get a list of all current postings    
def find_allPostings(conn):
    curs = conn.cursor()
    curs.execute('''select pid,name,pay,minHours, 
    location from project;''')
    allPostings = curs.fetchall()
    return allPostings;

#SQL query to get specifically email of a student with a given name 
def get_email(conn, name):
    curs = conn.cursor()
    curs.execute('''select email from user where name like %s;''', [name + '%'])
    email = curs.fetchone()
    return email[0]

   
if __name__ == '__main__':
    conn = getConn('clickdb')
    #addSkill(conn, "student2@gmail.com", "editing")
    #print(removeSkill(conn, "student1@gmail.com", "math tutoring"))