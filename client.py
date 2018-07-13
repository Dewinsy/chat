# This is a joint project between Daisy, Arthur and Tom
#
# This program implements a client application that sends and receives messages from another
# client through a server using a command line interface.
#
# Contacts:
#   Arthur +256-758-855-695 <athurstaurtleo@hotmail.com>
#   Daisy  +256-751-300-440 <mushdaisy71@gmail.com>

IP="0.0.0.0"
PORT=4546

import requests as REQ, json
import sys

#jencode = json.JSONEncoder().encode # not needed!
jdecode = json.JSONDecoder().decode

ID = 0

def get_users_in_system():
    return jdecode(REQ.get("http://%s:%d/users"%(IP,PORT)).text)
    
def login(username):
    global ID
    ID = jdecode(REQ.post("http://%s:%d/login"%(IP,PORT), json={"uname":username}).text)["id"]

def register(username):
    global ID
    ID = jdecode(REQ.post("http://%s:%d/register"%(IP,PORT), json={"uname":username}).text)["id"]

def read_inbox():
    if not ID:
        print "please first login or register to get your inbox!"
        return
    
    reply = jdecode(REQ.post("http://%s:%d/read_inbox"%(IP,PORT), json={"id":ID}).text)
    
    if not reply["status"]:
        print reply["log"]
        return
    
    for msg in reply["messages"]:
        print "(%s) %s:: %s"%(msg[0], msg[1], msg[2])
    
    if len(reply["messages"])==0:
        print "sorry, you dont have any messages"

def post_message():
    if not ID:
        print "please first login or register to send a message!"
        return

    users = get_users_in_system()
    
    user_list = []
    counter = 1
    
    print "users in the system:"
    for user in users:
        print "    %d) %s"%(counter, user[1])
        user_list.append(user[0])
        counter += 1
    
    recepients = raw_input("please enter recepient numbers(separate with commas): ").strip().split(",")
    
    try:
        recepients = [int(recepient) for recepient in recepients]
    except:
        print "invalid input"
        return
        
    actual_recepients = []
    for recepient in recepients:
        recepient -= 1
        if recepient<0 or recepient>=len(user_list):
            print "invalid entry found...please try again"
            post_message()

        if user_list[recepient] not in actual_recepients:
            actual_recepients.append(user_list[recepient])

    msg = raw_input("type your message here: ")
    while not msg:
        msg = raw_input("type your message here: ")
    
    reply = jdecode(REQ.post("http://%s:%d/post_message"%(IP,PORT), json={
        "id":ID,
        "recepients": actual_recepients,
        "msg":msg
    }).text)    

    if reply["status"]:
        print "message sent successfully"
    else:
        print "sorry, message not posted. reas: %s"%reply["log"]

def logout():
    sys.exit("goodbye!")

while 1:
    entry = raw_input("enter <r> to register or <l> to login: ")
    if entry=="l":
        login(raw_input("please enter your username: "))
        if not ID:
            print "invalid username given!"
    elif entry=="r":
        register(raw_input("please enter your desired username: "))
        if not ID:
            print "sorry, that username is already taken!"
    elif entry=="x":
        logout()
    else:
        print "incorrect input!"
    
    if ID:
        break

while 1:
    action = raw_input("enter <p> to post message or <g> to get inbox: ")
    if action=="p":
        post_message()
    elif action=="g":
        read_inbox()
    elif action=="x":
        logout()
    else:
        print "incorrect input. please follow instructions!"
    
#login(raw_input("your username: "))
#post_message()
#read_inbox()
