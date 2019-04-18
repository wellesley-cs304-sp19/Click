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

#put rest of routes/functions here

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)