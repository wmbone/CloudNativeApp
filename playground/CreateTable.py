import sqlite3
conn = sqlite3.connect('mydb.db')

try:
    c = conn.cursor()
#    c.execute('''create table apirelease(buildtime date, version varchar(30) primary key,
#            links varchar2(30), methods varchar2(30))''')
#    c.execute('''INSERT INTO apirelease(buildtime,version,links,methods)
#    VALUES ("09/10/2020","0.01","/api/v1","all")''')
#    c.execute('''drop table users''')
#    c.execute('''CREATE TABLE users(
#            username varchar2(30),
#            email varchar2(30),
#            password varchar2(30), full_name varchar(30),
#            id integer primary key autoincrement)''')
    c.execute('''CREATE TABLE tweets(
        id integer primary key autoincrement,
        username varchar2(30),
        body varchar2(30),
        tweet_time date)''')
#
#    c.execute('''INSERT INTO users(username,full_name,email,password,id)
#            VALUES ("bone","Raymond Chiu","mail@123.com","12345","1")''')
    c.execute('''SELECT * from users where id=1''')
    print("Print all rolls in users", c.fetchall())
    conn.commit()
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table")
    print("Exception class is: ", error.__class__)
    print("Exception is", error.args)
finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")