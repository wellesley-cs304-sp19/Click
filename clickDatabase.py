#CS304 Project
#Dana, Erica, and Gabby

import sys
import MySQLdb
import threading
from connection import getConn
from threading import lock
import re

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

########################GAB'S Functions
#adds a new user
def addUser(conn,email,password):
    curs=conn.cursor()
    newrow=curs.execute('''insert into user(email,password) values (%s,%s)''',[email,password])
    return newrow

#add a new job posting
def addProject(conn,project_dict):
    curs = conn.cursor()
    curs.execute('''insert into project (name,minHours,pay,location) values (%s,%s,%s,%s);''',[project_dict['name'],project_dict['minHours'],project_dict['pay'],project_dict['location']])
    curs.execute('''select last_insert_id();''')
    result=curs.fetchall()
    return(result[0][0])


   
if __name__ == '__main__':
    conn = getConn('clickdb')
    #addSkill(conn, "student2@gmail.com", "editing")
    #print(removeSkill(conn, "student1@gmail.com", "math tutoring"))
    #studentSkills(conn, "student1@gmail.com")