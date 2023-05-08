from flask import Flask, render_template, request, redirect, url_for, session

# Flask - new Flask web application
# render_template - This renders the template for the web pages
# request - get data from the user's request
# redirect - redirect to a different web page
# url_for - generates a URL to a specific function
# session - store user-specific data.
#

import sqlite3

# python library that allows you to store and retrieve data from an SQL database.

app = Flask(__name__)  # creates a new Flask application
@app.route('/')
def index():
    return 'Web App with Python Flask!'
    app.run(host='0.0.0.0', port=81)

db_path = 'CFGfinalprojectdatabase.db' # assigns the string value to CFG final project DB

@app.route('/')  # navigates to the root URL of the application called homepage
def homepage():
    return render_template('moodtrackerhomepage.html') # this render_template will look for a file and return HTML page


# right ladies just a note for myself - we need to make @app.routes for the likes of create account, logins, daily record page, calander overview page etc