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

'''Gets student's information (name, email) from database'''
def getStudent(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''Select name, email from user where email = %s''', [email])
    return curs.fetchone()

'''Returns results of SQL query to get student's skills from the database'''   
def studentSkills(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    #use inner join to get list of skills
    curs.execute('''select skill from skills inner join hasSkill using (sid)
    where hasSkill.email = %s''', [email])
    return curs.fetchall()
    
'''Removes skill from student'''  
def removeSkill(conn, email, skill):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    nr = curs.execute('''delete from hasSkill where sid = 
    (select sid from skills where skill = %s) and email = %s''', [skill, email])
    return nr

'''Adds skill to student'''    
def addSkill(conn, email, skill):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute('''Select sid from skills where skill = %s''', [skill])
    skillQuery = curs.fetchone() #stores results from query to get skills
    #if skill not in skills table, add it
    if skillQuery == None:
        curs.execute('''insert into skills(skill) values (%s)''', [skill])
        curs.execute('''select last_insert_id()''')
        skillNum = curs.fetchone()['last_insert_id()']
    else:
        skillNum = skillQuery['sid'] #set skillNum to sid from skillQuery
    #continue with inserting email and skill into hasSkill table
    nr = curs.execute('''insert into hasSkill(email, sid) values (%s, %s)''', [email, skillNum])
    return nr
    
#adds a new user
def addUser(conn,email,password):
    curs=conn.cursor()
    newrow=curs.execute('''insert into user(email,password) values (%s,%s)''',[email,password])
    return newrow
    
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
    #addSkill(conn, "student2@gmail.com", "public speaking")
    #print(removeSkill(conn, "student1@gmail.com", "math tutoring"))
    #print(studentSkills(conn, "student1@gmail.com"))
