# Import libraries and modules
import json

from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, request
#from flask_mysqldb import MySQL
import sqlite3
from sqlite3 import Error
#import createTable
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


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


if __name__ == '__main__':
    app.run(debug=True)