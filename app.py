# Import libraries and modules
import json
#import uuid
#import logging
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, request
#from flask_mysqldb import MySQL
import sqlite3
from sqlite3 import Error
#import createTable
#from flask_sessionstore import Session
#from flask_session_captcha import FlaskSessionCaptcha
#from pymongo import MongoClient
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

'''# Database Config
# If your mongodb runs on a different port
# change 27017 to that port number
mongoClient = MongoClient('localhost', 27017)

# Captcha Configuration
app.config["SECRET_KEY"] = uuid.uuid4()
app.config['CAPTCHA_ENABLE'] = True

# Set 5 as character length in captcha
app.config['CAPTCHA_LENGTH'] = 5

# Set the captcha height and width
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60
app.config['SESSION_MONGODB'] = mongoClient
app.config['SESSION_TYPE'] = 'mongodb'

# Enables server session
Session(app)

# Initialize FlaskSessionCaptcha
captcha = FlaskSessionCaptcha(app)'''

'''messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]'''

'''Setup connection'
app.config['MYSQL_HOST'] = 'Alex-Laptop'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Cyberpunk2077'
app.config['MYSQL_DB'] = 'ecommerce'

mysql = MySQL(app)'''


'''messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]'''

#Global Variable
def global_var(Uname):
    global globalUsername
    globalUsername = Uname
    return globalUsername

'''def global_var2(attempt):
    global globalAttempt
    globalAttempt = attempt - 1
    return globalAttempt'''

'''def global_var3(start):
    global Attempt
    Attempt = start
    return Attempt
globalAttempt = global_var2(3)
print('globalAttempt = ', globalAttempt)'''

'''def insert():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('INSERT INTO users VALUES("Alexander", "Alex_2023@")')
    con.commit()
    con.close()'''

#insert()

'''def droptable():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('DROP TABLE users')
    con.commit()
    con.close()
    print ('Table dropped successfully')'''

#droptable()
@app.route('/view')
def view():
    database = r"database.db"
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    userrows = cur.fetchall()
    print("2. Query all users")
    print(userrows)
    cur.execute("SELECT * FROM products")
    productrows = cur.fetchall()
    print("2. Query all products")
    print(productrows)
    data = productrows + userrows
    return jsonify(data)
    #return render_template('view.html', rows=rows)
# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            age = request.form['age']
            return redirect(url_for('about', age=age))
    except ValueError:
        flash('Age is required!')
    return render_template('index.html')

# About page and passing variable to html (age) required
@app.route('/about/<int:age>')
def about(age):
    age = age
    return render_template('about.html', age=age)

# Login page route with POST and GET methods and SQL query to check username and password
@app.route('/login', methods=['GET', 'POST'])
def login():
    #globalAttempt = global_var2(attempt=3)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                #cur = mysql.connection.cursor()
                #cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
                user = cur.fetchall()
                cur.close()
                User=user[0]
                Uname=User[0]
                Pword=User[1]
                if Uname == username and Pword == password:
                    global_var(Uname)
                    return redirect(url_for('loginsuccess', globalUsername = Uname))
                else:
                    #globalAttempt = global_var2(globalAttempt)
                    flash('Username or Password is incorrect!')
                    #print(globalAttempt)
            except IndexError:
                #globalAttempt = global_var2(globalAttempt)

                flash('Username or Password is incorrect!')
                #print(globalAttempt)
    return render_template('login.html')

# Products page route with SQL query to get all products from products table in ecommerce database
@app.route('/products')
def products():
    '''cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products2')
    data = cur.fetchall()
    cur.close()'''
    database = r"database.db"
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    #return jsonify(data)
    return render_template('products.html', data1=data)

#Verify that user has logged in successfully
@app.route('/loginscucess/<globalUsername>')
def loginsuccess(globalUsername):
    globalUsername = globalUsername
    return render_template('loginsuccess.html', globalUsername = globalUsername)

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                #cur = mysql.connection.cursor()
                #cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                cur.close()
                if user:
                    flash('Username already exists!')
                else:
                    if password != confirmPassword:
                        flash('Passwords do not match!')
                    else:
                        cur = conn.cursor()
                        cur.execute('INSERT INTO users VALUES(?, ?)', (username, password))
                        conn.commit()
                        cur.close()
                        print(username)
                        return redirect(url_for('createaccountsuccess', globalUsername = username))
            except IndexError:
                flash('Username or Password is incorrect!')
    return render_template('createaccount.html')

@app.route('/createaccountsuccess/<globalUsername>')
def createaccountsuccess(globalUsername):
    globalUsername = globalUsername
    return render_template('createaccountsuccess.html', globalUsername = globalUsername)

'''@app.route('/testcaptcha', methods=['GET', 'POST'])
def testcaptcha():
    if request.method == "POST":
        if captcha.validate():
            return "success"
        else:
            return "fail"

    return render_template("testcaptcha.html")'''

@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    #globalUsername = globalUsername
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        oldPassword = request.form['oldPassword']
        confirmPassword = request.form['confirmPassword']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                #cur = mysql.connection.cursor()
                #cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                usertuple = user[0]
                userpwd = usertuple[1]
                print("User:", usertuple)
                cur.close()
                if not user or userpwd != oldPassword:
                    flash('Username does not exist or original password is incorrect!')
                else:
                    if password != confirmPassword:
                        flash('Passwords do not match!')
                    else:
                        cur = conn.cursor()
                        cur.execute('UPDATE users SET password = ? WHERE username = ?', (password, username))
                        conn.commit()
                        cur.close()
                        print(username)
                        return redirect(url_for('changepasswordsuccess', globalUsername = username))
            except IndexError:
                flash('Username or Password is incorrect!')

    return render_template('changepassword.html')

@app.route('/changepasswordsuccess/<globalUsername>')
def changepasswordsuccess(globalUsername):
    globalUsername = globalUsername
    return render_template('changepasswordsuccess.html', globalUsername = globalUsername)

@app.route('/changeusername', methods=['GET', 'POST'])
def changeusername():
    #globalUsername = globalUsername
    if request.method == 'POST':
        username = request.form['username']
        newUsername = request.form['newUsername']
        confirmUsername = request.form['confirmUsername']
        password = request.form['password']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                #cur = mysql.connection.cursor()
                #cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                usertuple = user[0]
                userpwd = usertuple[1]
                print("User:", usertuple)
                cur.close()
                if not user or newUsername != confirmUsername or userpwd != password or not newUsername or not confirmUsername:
                    flash('Original Username does not exist, usernames do not match or password is incorrect!')
                else:
                    cur = conn.cursor()
                    cur.execute('UPDATE users SET username = ? WHERE username = ?', (newUsername, username))
                    conn.commit()
                    cur.close()
                    print(username)
                    return redirect(url_for('changeusernamesuccess', globalUsername = newUsername))
            except IndexError:
                flash('Username or Password is incorrect!')

    return render_template('changeusername.html')

@app.route('/changeusernamesuccess/<globalUsername>')
def changeusernamesuccess(globalUsername):
    globalUsername = globalUsername
    return render_template('changeusernamesuccess.html', globalUsername = globalUsername)

@app.route('/deleteaccount', methods=['GET', 'POST'])
def deleteaccount():
    #globalUsername = globalUsername
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                #cur = mysql.connection.cursor()
                #cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                usertuple = user[0]
                userpwd = usertuple[1]
                print("User:", usertuple)
                cur.close()
                if not user or userpwd != password or password != confirmPassword or not password or not confirmPassword:
                    flash('Username does not exist or password is incorrect!')
                else:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM users WHERE username = ?', (username,))
                    conn.commit()
                    cur.close()
                    print(username)
                    return redirect(url_for('deleteaccountsuccess', globalUsername = username))
            except IndexError:
                flash('Username or Password is incorrect!')

    return render_template('deleteaccount.html')

@app.route('/deleteaccountsuccess/<globalUsername>')
def deleteaccountsuccess(globalUsername):
    globalUsername = globalUsername
    return render_template('deleteaccountsuccess.html', globalUsername = globalUsername)


if __name__ == '__main__':
    app.run(debug=True)