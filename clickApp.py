#CS304 Project
#Dana, Erica, and Gabby

from flask import (Flask, url_for, render_template, request, redirect, flash)
import random,math
import clickDatabase

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