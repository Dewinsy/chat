#Program that uses database to store username, IDs and messages of different users that are registered in the system.
#
#Written by:
#   Mushabe Daisy
#
#Contacts:
#   +256-751-300-440
#   mushdaisy71@gmail.com


import sqlite3 as sql,sys, time
FNAME = "user_details.db"

def init ():
    db = sql.connect(FNAME)
    cur=db.cursor()
    stmt="""create table if not exists users_details(
    ID int primary key not null,
    username varchar(30) not null,
    last_fetch_time real not null
    )"""
    cur.execute(stmt)
    db.commit()
    
    cur=db.cursor()
    stmt="""create table if not exists messages(
    message_to int not null,
    message_from varchar(30) not null,
    message text not null,
    time_sent_human_form varchar(5) not null,
    message_time_in_seconds real not null
    )"""
    cur.execute(stmt)
    db.commit()
    
    return db,cur
    
def write_user_details(db, cur, uid, uname, last_fetch_time=0):
    cur = db.cursor()
    stmt = """
    insert into users_details values(?,?,?)
    """
    try:
        cur.execute(stmt,(uid,uname,last_fetch_time))
        db.commit()
        return True
    except:
        return False
        
#db,cur =init()
#users = write_user_details(db,cur,"Arthur2",59966)
#print users

def read_user_details(db,cur):
    cur.execute("select ID, username from users_details")
    rows = cur.fetchall()
    rows.sort(key=lambda r:r[1]) #this sorts the users' names in the system alphabtically
    return rows
    
#users = read_user_details(*init())     
#print users    

def get_inbox(db, cur, uid):
    cur.execute("select last_fetch_time from users_details where ID = ?",(uid,))
    last_fetch_time = cur.fetchone()
    if not last_fetch_time:
        return []
        
    last_fetch_time = last_fetch_time[0]

    t=time.time()
    cur.execute("""
        select time_sent_human_form,message_from,message from messages where 
        (message_to = ?) and (message_time_in_seconds > ?)""",
        (uid,last_fetch_time)
    )
    messages = cur.fetchall()
    
    cur.execute("update users_details set last_fetch_time=? where ID=?",(t,uid))
    db.commit()
    return messages
        
#db,cur = init()        
#inbox = get_inbox(db, cur, 59966) 
#print inbox   
    
def save_message(db, cur, uid, uname, message ):
    cur = db.cursor()
    stmt = """
    insert into messages values(?,?,?,?,?)
    """
    cur.execute(stmt,(uid, uname, message, time.asctime(), time.time()))
    db.commit()
    
#db,cur = init()
#msgs = save_message(db, cur, 59966, "mush" ,"Hello:)")
#print msgs
