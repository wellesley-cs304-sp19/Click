#CS304 Project
#Dana, Erica, and Gabby

from flask import (Flask, url_for, render_template, request, redirect, flash,session)
<<<<<<< HEAD
=======
from datetime import date
>>>>>>> origin/master
import random,math
import MySQLdb
import sys
import bcrypt
import clickDatabase
<<<<<<< HEAD
=======
from connection import getConn
>>>>>>> origin/master
from functools import wraps
import os

app = Flask(__name__)

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
<<<<<<< HEAD
                           
conn = clickDatabase.getConn('clickdb')
=======
                          
>>>>>>> origin/master

#route to the home page
@app.route("/")
def home():
    return render_template('home.html')
    
<<<<<<< HEAD
=======

>>>>>>> origin/master
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
=======
    
>>>>>>> origin/master
#route to the login page
@app.route('/login/',methods=['GET','POST'])
def login():
    #the code below works well
<<<<<<< HEAD
    #return render_template('login.html')
    
    #somehow the code below gives Bad Request: The browser (or proxy) sent a request that this server could not understand.
    try:
=======
    if request.method=='GET':
        return render_template('login.html')
    else:
        print("test enter")
>>>>>>> origin/master
        username=request.form['username']
        password=request.form['password']
        conn=clickDatabase.getConn('clickdb')
        curs=conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('select password from user where email=%s',[username])
        row=curs.fetchone()
        if row is None:
<<<<<<< HEAD
            flash('Login failed. Please register or try again')
            return redirect(url_for('home'))
        hashed=row['password']
        if bcrypt.hashpw(password.encode('utf-8'),hashed.encode('utf-8'))==hashed:
=======
            print("test enter1")
            flash('Login failed. Please register or try again')
            return redirect(url_for('home'))
        hashed=row['password']
        if (bcrypt.hashpw(password.encode('utf-8'),hashed.encode('utf-8'))==hashed.encode('utf-8')):
            print("test enter2")
>>>>>>> origin/master
            flash('Successfully logged in as'+username)
            session['username']=username
            session['logged_in']= True
            return redirect(url_for('home'))
        else:
<<<<<<< HEAD
            flash('Login failed. Please register or try again')
            return redirect(url_for('login'))
    except Exception as err:
        flash('From submission error'+str(err))
        return redirect(url_for('home'))
        
        
#route to the register page
@app.route('/register/')
def register():
=======
            print("test enter3")
            flash('Login failed. Please register or try again')
            return redirect(url_for('login'))
        #except Exception as err:
            #flash('From submission error'+str(err))
            #return render_template('login.html')
            #return redirect(url_for('home'))

@app.route('/loginPage/',methods=["POST"])  
def redirectToLogin():
    '''renders login.html where user can login or register'''
    return render_template('login.html')        
        
#route to the register page
@app.route('/register/', methods=["POST"])
def register():
    '''allows user to register by creating a username and password;
    if username is unique, encrypts passwords and store it'''
>>>>>>> origin/master
    try:
        username=request.form['username']
        password1=request.form['password1']
        password2=request.form['password2']
        if password1 != password2:
            flash('Passwords do not match.')
            return redirect(url_for('login'))
        hashed=bcrypt.hashpw(password1.encode('utf-8'),bcrypt.gensalt())
        #hashed=password1
<<<<<<< HEAD
        conn=clickDatabase.getConn('clickdb')
=======
        conn=getConn()
>>>>>>> origin/master
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
<<<<<<< HEAD
=======
    '''logging out the current user'''
>>>>>>> origin/master
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
        
<<<<<<< HEAD
#route to page that student sees when first log in
=======
'''route to page that student sees when first log in'''
>>>>>>> origin/master
@app.route("/student/<email>")
#@login_required
def studentPage(email):
    return render_template('student.html',
                            email=email)
<<<<<<< HEAD
=======
                            
@app.route('/reset/', methods=['GET', 'POST'])
def reset():
    '''clears all filters and sorting and displays original tables'''
    resetType = request.form.get("submit-reset")
    #in students.html, reset students; return master list of students
    if (resetType == "Reset Students"):
        return redirect('students')
    #in project.html, reset projects; return master list of projects
    else: 
        return redirect('projects')
>>>>>>> origin/master

#route to page that job poster sees when first log in
@app.route("/jobPoster/<email>")
def jobPosterPage(email):
    return render_template('jobPoster.html',
                            email=email)                           

<<<<<<< HEAD
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
=======
'''Route to page that allows student to view profile and add skills.
   The student profile is for the student that is currently logged in.
'''
@app.route("/studentProfile/<email>", methods = ['GET'])
#@login_required
def studentProfile(email):
    conn = clickDatabase.getConn('clickdb')
    studentInfo = clickDatabase.getStudent(conn, email)
    skills = clickDatabase.studentSkills(conn, email)
    #renders page with all information about student in database
    return render_template('studentProfile.html',
                        name = studentInfo['name'],
                        email = studentInfo['email'],
                        active = studentInfo['active'],
                        skills = skills)
 
'''Route to page to update student profile'''                             
@app.route("/studentUpdate/<email>", methods = ['GET', 'POST'])
def studentUpdate(email):
    conn = clickDatabase.getConn('clickdb')
    studentInfo = clickDatabase.getStudent(conn, email)
    skills = clickDatabase.studentSkills(conn, email)
    #if GET, renders page with given information as default values in form
    if request.method == 'GET':
        return render_template('studentUpdate.html',
                            name = studentInfo['name'],
                            email = studentInfo['email'],
                            active = studentInfo['active'],
                            skills = skills)
    #if POST, updates profile
    else:
        # if student updates name, email, or active status
        if request.form['submit'] == 'Update Personal Information':
            newName = request.form.get('studentName')
            newEmail = request.form.get('studentEmail')
            newActive = request.form.get('studentActive')
            clickDatabase.updateStudentProfile(conn, email, newEmail, newName, newActive)
            flash("Profile successfully updated")
            return redirect(url_for('studentUpdate', email=newEmail))
        # if student removes a skill
        elif request.form['submit'] == 'Remove':
            skill = request.form.get('skill')
            clickDatabase.removeSkill(conn, email, skill)
            return redirect(url_for('studentUpdate',
                            email = studentInfo['email']))
        #adding skill
        elif request.form['submit'] == 'Add skill':
            #try and except to handle errors if user tries to enter a
            #skill they've already added to their profile
            try:
                newSkill = request.form.get('newSkill')
                clickDatabase.addSkill(conn, email, newSkill)
                return redirect(url_for('studentUpdate',
                                email = studentInfo['email']))
            except:
                flash("Error. Skill may already be in your profile.")
                return redirect(url_for('studentUpdate',
                                email = studentInfo['email']))
        else:
            return redirect(url_for('studentProfile',
                            email = studentInfo['email']))
                            
@app.route("/jobs", methods = ['GET', 'POST'])
def jobs():
    conn = clickDatabase.getConn('clickdb')
    if request.method == 'GET':
        jobs = clickDatabase.getJobs(conn)
        return render_template('jobs.html', jobs = jobs)
    else:
        if request.form['submit'] == 'Search':
            search = request.form.get('searchJobs')
            filteredJobs = clickDatabase.searchJobs(conn, search)
            return render_template('jobs.html', jobs = filteredJobs)

#route to page that allows job poster to see his/her current postings     
@app.route("/posting/<pid>", methods = ['GET', 'POST'])
def posting(pid):
    conn = clickDatabase.getConn('clickdb')
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
>>>>>>> origin/master
    conn = clickDatabase.getConn('clickdb')
    if request.method == 'POST':
    
        # checking database to see if the given pid is in use 
<<<<<<< HEAD
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
=======
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
>>>>>>> origin/master
    
# returns true when a SQL query's result is not empty
def isValid(results):
    return results != None
    
# select page form handling
<<<<<<< HEAD
@app.route('/selectProject/', methods=['GET','POST'])
def select_project():
    conn = clickDatabase.getConn('clickdb')
    pid = request.form.get('select-name') ###this line may not work
    if isValid(pid):
        return redirect(url_for('updateProject', pid=pid))
    else: 
        flash('Please select a project')
        return render_template('selectProject.html')
=======
@app.route('/selectPosting/', methods=['GET','POST'])
def select_posting():
    conn = clickDatabase.getConn('clickdb')
    pid = request.form.get('select-name') ###????
    if isValid(pid):
        return redirect(url_for('updatePosting', pid=pid))
    else: 
        flash('Please select a project posting')
        return render_template('selectPosting.html')
>>>>>>> origin/master
        
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
<<<<<<< HEAD
        return redirect(url_for('updateProject', email=email))
=======
        return redirect(url_for('updatePosting', email=email))
>>>>>>> origin/master
    else: 
        flash('Requested student does not exist')
        return render_template('searchStudent.html')

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8080)
