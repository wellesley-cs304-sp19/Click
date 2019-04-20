#CS304 Project
#Dana, Erica, and Gabby

from flask import (Flask, url_for, render_template, request, redirect, flash,session)
import random,math
import MySQLdb
import sys
import bcrypt
import clickDatabase
from functools import wraps

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

#route to the login page
@app.route("/login")
def login():
    return render_template('login.html')

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
    
#route to the register page
@app.route('/register')
def register():
    try:
        username=request.form['username']
        password1=request.form['password1']
        password2=request.form['password2']
        if password1 != password2:
            flash('Passwords do not match.')
            return redirect(url_for('login'))
        hashed=bcrypt.hashpw(password1.encode('utf-8'),bcrypt.gensalt())
        conn=clickDatabase.getConn('c9')
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
        
#route to page that student sees when first log in
@app.route("/student/<email>")
def studentPage(email):
    return render_template('student.html',
                            email=email)

#route to page that allows student to view profile and add skills    
@app.route("/studentProfile/<email>", methods = ['GET', 'POST'])
def studentProfile(email):
    #if GET, renders page with all information about student in database
    if request.method == 'GET':
        studentInfo = clickDatabase.getStudent(conn, email)
        skills = clickDatabase.studentSkills(conn, email)
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
            return render_template('studentProfile.html',
                            name = studentInfo['name'],
                            email = studentInfo['email'],
                            skills = skills)
        #adding skill
        else:
            newSkill = request.form.get('newSkill')
            clickDatabase.addSkill(conn, email, newSkill)
            return render_template('studentProfile.html',
                            name = studentInfo['name'],
                            email = studentInfo['email'],
                            skills = skills)

#put rest of routes/functions here

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)