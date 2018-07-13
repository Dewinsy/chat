#Program that uses database to store details.
#
#Written by:
#   Mushabe Daisy
#
#Contacts:
#   +256-751-300-440
#   mushdaisy71@gmail.com


import sqlite3 as sql,sys
FNAME = "data.db"

try:
    db = sql.connect(FNAME)
except:
    sys.exit("ERROR!")

cur=db.cursor()
stmt="""create table if not exists employee_details(
username varchar(30) primary key not null,
pswd varchar(30) not null,
contact varchar(30) not null,
email varchar(100)

)"""
cur.execute(stmt)
db.commit()

stmt="""
insert into employee_details values(?,?,?,?)
"""
#cur.execute(stmt,("Tom","6767","0758855695", None))
#db.commit()
cur.execute("select* from employee_details")
rows = cur.fetchall()
print rows

cur.execute("select username,contact from employee_details")
rows = cur.fetchall()
print rows

cur.execute(   "select* from employee_details where username=?", ("Arthur2",)     )
rows = cur.fetchall()
print rows

cur.execute("select* from employee_details where username like ?", ("%t%",))
rows = cur.fetchall()
print rows
    
cur.execute("select* from employee_details where username like ?", ("t%",))
rows = cur.fetchall()
print rows
