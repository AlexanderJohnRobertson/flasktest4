import sqlite3

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE users(username varchar(20) primary key, password varchar(20) not null)')
#conn.execute('CREATE TABLE products(productID varchar(20) primary key, productName varchar(20) not null, quantity int(5) not null, price decimal(5,2) not null,prodImage text(50) not null)')
print('Table created successfully')
conn.close()

