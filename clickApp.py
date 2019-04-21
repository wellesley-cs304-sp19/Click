#CS304 Project
#Dana, Erica, and Gabby

from flask import (Flask, url_for, render_template, request, redirect, flash,session)
import random,math
import MySQLdb
import sys
import bcrypt
import clickDatabase
from functools import wraps
<<<<<<< HEAD
=======
import os
>>>>>>> 61191da32f7f52508101364fc5eef7b17dd0c35a

app = Flask(__name__)

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
                           
conn = clickDatabase.getConn('clickdb')

#route to the home page
@app.route("/")
def home():
    return render_template('home.html')
<<<<<<< HEAD

#route to the login page
@app.route("/login")
def login():
    return render_template('login.html')

=======
    
def getConn(db):
    conn = MySQLdb.connect(user='ubuntu',host='localhost',password='',db=db)
    conn.autocommit(True)
    return conn
    
>>>>>>> 61191da32f7f52508101364fc5eef7b17dd0c35a
'''Since in the future, we want to have a user visiting
    a site to be redirected to the login page if they are
    not already logged in. We use a decorator to solve 
    this problem. 
'''
#method learned from flask.pocoo.org
def login_required(f):
    @wraps(f)
    def decorated_fcn():
        if 'logged_in' in session:
            return f()
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return decorated_fcn()
<<<<<<< HEAD
    
#route to the register page
@app.route('/register')
=======

#route to the login page
@app.route('/login/',methods=['GET','POST'])
def login():
    #the code below works well
    #return render_template('login.html')
    
    #somehow the code below gives Bad Request: The browser (or proxy) sent a request that this server could not understand.
    try:
        username=request.form['username']
        password=request.form['password']
        conn=getConn('clickdb')
        curs=conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('select password from user where email=%s',[username])
        row=curs.fetchone()
        if row is None:
            flash('Login failed. Please register or try again')
            return redirect(url_for('home'))
        hashed=row['password']
        if bcrypt.hashpw(password.encode('utf-8'),hashed.encode('utf-8'))==hashed:
            flash('Successfully logged in as'+username)
            session['username']=username
            session['logged_in']= True
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please register or try again')
            return redirect(url_for('login'))
    except Exception as err:
        flash('From submission error'+str(err))
        return redirect(url_for('home'))
        
        
#route to the register page
@app.route('/register/')
>>>>>>> 61191da32f7f52508101364fc5eef7b17dd0c35a
def register():
    try:
        username=request.form['username']
        password1=request.form['password1']
        password2=request.form['password2']
        if password1 != password2:
            flash('Passwords do not match.')
            return redirect(url_for('login'))
        hashed=bcrypt.hashpw(password1.encode('utf-8'),bcrypt.gensalt())
<<<<<<< HEAD
        conn=clickDatabase.getConn('c9')
=======
        #hashed=password1
        conn=getConn('clickdb')
>>>>>>> 61191da32f7f52508101364fc5eef7b17dd0c35a
        curs=conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('select email from user where email=%s',[username])
        row=curs.fetchone()
        if row is not None:
            flash('This email has already been used')
            return redirect(url_for('login'))
        curs.execute('insert into user(email,password) values (%s,%s)',[username,hashed])
        session['username']=username
        session['logged_in']=True
        flash('Successfully logged in as'+username)
<<<<<<< HEAD
        return redirect(url_for('login'))
    except Exception as err:
        flash('From submission error'+str(err))
        return redirect(url_for('index'))
        
#route to page that student sees when first log in
@app.route("/student/<email>")
=======
        return redirect(url_for('home'))
    except Exception as err:
        flash('From submission error'+str(err))
        return redirect(url_for('home'))

#route to logout
@app.route('/logout/')
def logout():
    try:
        if 'username' in session:
            username = session['username']
            session.pop('username')
            session.pop('logged_in')
            flash('You are logged out')
            return redirect(url_for('home'))
        else:
            flash('You are not logged in. Please login or register')
            return redirect( url_for('home') )
    except Exception as err:
        flash('Error Message: '+str(err))
        return redirect( url_for('home') )
        
#route to page that student sees when first log in
@app.route("/student/<email>")
#@login_required
>>>>>>> 61191da32f7f52508101364fc5eef7b17dd0c35a
def studentPage(email):
    return render_template('student.html',
                            email=email)

<<<<<<< HEAD
#route to page that job poster sees when first log in
@app.route("/jobPoster/<email>")
def jobPosterPage(email):
    return render_template('jobPoster.html',
                            email=email)                           

#route to page that allows student to view profile and add skills    
@app.route("/studentProfile/<email>", methods = ['GET', 'POST'])
def studentProfile(email):
    #if GET, renders page with all information about student in database
    if request.method == 'GET':
        studentInfo = clickDatabase.getStudent(conn, email)
        skills = clickDatabase.studentSkills(conn, email)
=======
#route to page that allows student to view profile and add skills    
@app.route("/studentProfile/<email>", methods = ['GET', 'POST'])
#@login_required
def studentProfile(email):
    studentInfo = clickDatabase.getStudent(conn, email)
    skills = clickDatabase.studentSkills(conn, email)
    #if GET, renders page with all information about student in database
    if request.method == 'GET':
        #studentInfo = clickDatabase.getStudent(conn, email)
        #skills = clickDatabase.studentSkills(conn, email)
>>>>>>> 61191da32f7f52508101364fc5eef7b17dd0c35a
        return render_template('studentProfile.html',
                            name = studentInfo['name'],
                            email = studentInfo['email'],
                            skills = skills)
    #if POST, either adding or removing a skill
    else:
        #removing skill
        if request.form['submit'] == 'Remove':
            skill = request.form.get('skill')
            clickDatabase.removeSkill(conn, email, skill)
<<<<<<< HEAD
            return render_template('studentProfile.html',
                            name = studentInfo['name'],
                            email = studentInfo['email'],
                            skills = skills)
=======
            return redirect(url_for('studentProfile',
                            email = studentInfo['email']))
>>>>>>> 61191da32f7f52508101364fc5eef7b17dd0c35a
        #adding skill
        else:
            newSkill = request.form.get('newSkill')
            clickDatabase.addSkill(conn, email, newSkill)
<<<<<<< HEAD
            return render_template('studentProfile.html',
                            name = studentInfo['name'],
                            email = studentInfo['email'],
                            skills = skills)

#put rest of routes/functions here

#route to page that allows job poster to see his/her current postings     
@app.route("/posting/<pid>", methods = ['GET', 'POST'])
def posting(pid):
    #if GET, renders page with all information about that posting in database
    if request.method == 'GET':
        postingInfo = clickDatabase.getPosting(conn, pid)
        return render_template('posting.html',
                            name = postingInfo['name'],
                            minHours = postingInfo['minHours'],
                            pay = postingInfo['pay'],
                            location = postingInfo['location'],
                            )

# insert page
@app.route('/insertPosting/')
def insertPosting():
    return render_template('insertPosting.html')

# insert page form handling 
@app.route('/insertPosting/', methods=['GET','POST'])
def submit_insertPosting():
    conn = clickDatabase.getConn('clickdb')
    if request.method == 'POST':
    
        # checking database to see if the given pid is in use 
        if (clickDatabase.search_posting_pid(conn, request.form['posting-pid'])) != None:
            flash('bad input: project\'s pid already in use.')
            return render_template('insertPosting.html')
        
        # checking if info is missing in input 
        if ((request.form['posting-pid'] == "") or (request.form['posting-name'] == "") 
        or (request.form['posting-pay'] == "") or (request.form['posting-minHours'] == "")
        or (request.form['posting-location'] == "")):
            if request.form['posting-pid'] == "":
                flash('missing input: project\'s pid is missing.')
                
        
            if request.form['posting-name'] == "":
                flash('missing input: name is missing.')
               
            if request.form['posting-pay'] == "": 
                flash('missing input: pay is missing.')
                
            if request.form['posting-minHours'] == "": 
                flash('missing input: minimum hours is missing.')
                
            if request.form['posting-location'] == "": 
                flash('missing input: location is missing.')
                
            return render_template('insertPosting.html')
            
        if ((request.form['posting-pid'] == "") and (request.form['posting-name'] == "") 
        and (request.form['posting-pay'] == "") and (request.form['posting-minHours'] == "")
        and (request.form['posting-location'] == "")):
            
            postingInfo = clickDatabase.search_posting_pid(conn, request.form['posting-pid'])
            if postingInfo == None: 
                clickDatabase.insert_posting(conn, request.form['posting-pid'], 
                request.form['posting-name'], request.form['posting-pay'],
                request.form['posting-minHours'], request.form['posting-location'])
                flash('Posting {name} was created successfully'.format(title=request.form['posting-name']))

            else:
                flash("Posting already exists")
            return redirect(url_for('updatePosting', pid = request.form['movie-posting']))

# setting up page with postings
@app.route('/selectPosting/')
def selectPosting():
    conn = clickDatabase.getConn('clickdb')
    allPostings = clickDatabase.find_allPostings(conn)
    return render_template('selectPosting.html', allPostings=allPostings)
    
# returns true when a SQL query's result is not empty
def isValid(results):
    return results != None
    
# select page form handling
@app.route('/selectPosting/', methods=['GET','POST'])
def select_posting():
    conn = clickDatabase.getConn('clickdb')
    pid = request.form.get('select-name') ###????
    if isValid(pid):
        return redirect(url_for('updatePosting', pid=pid))
    else: 
        flash('Please select a project posting')
        return render_template('selectPosting.html')
        
# search page
@app.route('/searchStudent/')
def searchStudent():
    return render_template('searchStudent.html')
    
# search page with form request handling   
@app.route('/searchStudent/', methods=['GET','POST'])
def search_student():
    name = request.form.get('search-name')
    conn = clickDatabase.getConn('clickdb')
    email = clickDatabase.get_email(conn, name)
    if isValid(email):
        return redirect(url_for('updatePosting', email=email))
    else: 
        flash('Requested student does not exist')
        return render_template('searchStudent.html')

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)
=======
            return redirect(url_for('studentProfile',
                            email = studentInfo['email']))

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)
>>>>>>> 61191da32f7f52508101364fc5eef7b17dd0c35a
