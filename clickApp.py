#CS304 Project
#Dana, Erica, and Gabby

from flask import (Flask, url_for, render_template, request, redirect, flash,session)
import random,math
import MySQLdb
import sys
import bcrypt
import clickDatabase
from functools import wraps
import os

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

#route to the login page
@app.route('/login/',methods=['GET','POST'])
def login():
    #the code below works well
    #return render_template('login.html')
    
    #somehow the code below gives Bad Request: The browser (or proxy) sent a request that this server could not understand.
    try:
        username=request.form['username']
        password=request.form['password']
        conn=clickDatabase.getConn('clickdb')
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
def register():
    try:
        username=request.form['username']
        password1=request.form['password1']
        password2=request.form['password2']
        if password1 != password2:
            flash('Passwords do not match.')
            return redirect(url_for('login'))
        hashed=bcrypt.hashpw(password1.encode('utf-8'),bcrypt.gensalt())
        #hashed=password1
        conn=clickDatabase.getConn('clickdb')
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
        return redirect(url_for('login'))
    except Exception as err:
        flash('From submission error'+str(err))
        return redirect(url_for('index'))

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
def studentPage(email):
    return render_template('student.html',
                            email=email)

#route to page that job poster sees when first log in
@app.route("/jobPoster/<email>")
def jobPosterPage(email):
    return render_template('jobPoster.html',
                            email=email)                           

#route to page that allows student to view profile and add skills    
@app.route("/studentProfile/<email>", methods = ['GET', 'POST'])
#@login_required
def studentProfile(email):
    studentInfo = clickDatabase.getStudent(conn, email)
    skills = clickDatabase.studentSkills(conn, email)
    #if GET, renders page with all information about student in database
    if request.method == 'GET':
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
            return redirect(url_for('studentProfile',
                            email = studentInfo['email']))
        #adding skill
        else:
            newSkill = request.form.get('newSkill')
            clickDatabase.addSkill(conn, email, newSkill)
            return redirect(url_for('studentProfile',
                            email = studentInfo['email']))

#route to page that allows job poster to see his/her current projects     
@app.route("/project/<pid>", methods = ['GET', 'POST'])
def project(pid):
    #if GET, renders page with all information about that project in database
    if request.method == 'GET':
        projectInfo = clickDatabase.getProject(conn, pid)
        return render_template('project.html',
                            name = projectInfo['name'],
                            minHours = projectInfo['minHours'],
                            pay = projectInfo['pay'],
                            location = projectInfo['location'],
                            )

# insert page
@app.route('/insertProject/')
def insertProject():
    return render_template('insertProject.html')

# insert page form handling 
@app.route('/insertProject/', methods=['GET','POST'])
def submit_insertProject():
    conn = clickDatabase.getConn('clickdb')
    if request.method == 'POST':
    
        # checking database to see if the given pid is in use 
        if (clickDatabase.search_project_pid(conn, request.form['project-pid'])) != None:
            flash('bad input: project\'s pid already in use.')
            return render_template('insertProject.html')
        
        # checking if info is missing in input 
        if ((request.form['project-pid'] == "") or (request.form['project-name'] == "") 
        or (request.form['project-pay'] == "") or (request.form['project-minHours'] == "")
        or (request.form['project-location'] == "")):
            if request.form['project-pid'] == "":
                flash('missing input: project\'s pid is missing.')
                
        
            if request.form['project-name'] == "":
                flash('missing input: name is missing.')
               
            if request.form['project-pay'] == "": 
                flash('missing input: pay is missing.')
                
            if request.form['project-minHours'] == "": 
                flash('missing input: minimum hours is missing.')
                
            if request.form['project-location'] == "": 
                flash('missing input: location is missing.')
                
            return render_template('insertProject.html')
            
        if ((request.form['project-pid'] == "") and (request.form['project-name'] == "") 
        and (request.form['project-pay'] == "") and (request.form['project-minHours'] == "")
        and (request.form['project-location'] == "")):
            
            projectInfo = clickDatabase.search_project_pid(conn, request.form['project-pid'])
            if projectInfo == None: 
                clickDatabase.insert_project(conn, request.form['project-pid'], 
                request.form['project-name'], request.form['project-pay'],
                request.form['project-minHours'], request.form['project-location'])
                flash('Project {name} was created successfully'.format(title=request.form['project-name']))

            else:
                flash("Project already exists")
            return redirect(url_for('updateProject', pid = request.form['project-pid']))

# setting up page with projects
@app.route('/selectProject/')
def selectProject():
    conn = clickDatabase.getConn('clickdb')
    allProjects = clickDatabase.find_allProjects(conn)
    return render_template('selectProject.html', allProjects=allProjects)
    
# returns true when a SQL query's result is not empty
def isValid(results):
    return results != None
    
# select page form handling
@app.route('/selectProject/', methods=['GET','POST'])
def select_project():
    conn = clickDatabase.getConn('clickdb')
    pid = request.form.get('select-name') ###this line may not work
    if isValid(pid):
        return redirect(url_for('updateProject', pid=pid))
    else: 
        flash('Please select a project')
        return render_template('selectProject.html')
        
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
        return redirect(url_for('updateProject', email=email))
    else: 
        flash('Requested student does not exist')
        return render_template('searchStudent.html')

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8080)
