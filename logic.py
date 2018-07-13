# This is a joint project between Daisy, Arthur and another guy
#
# The logic defined here implements an SMS-like python command-line application
# in which a server stores and forwards messages to clients.
#
# the main lesson to be learned here is how to coordinate data between one server
# and two or more clients, as this is what happens in real world
#
# Contacts:
#   Arthur +256-758-855-695 <athurstaurtleo@hotmail.com>
#   Daisy  +256-751-300-440 <mushdaisy71@gmail.com>

import time, random, json
import sms_data

jencode = json.JSONEncoder().encode
jdecode = json.JSONDecoder().decode

class CustomRequest:
    def __init__(self, request):
        payload = request.form.get("json-payload","{}")
        self.json = jdecode(payload)
        

def generate_ID():
    """
    generate a random number from 10000 to 99999
    """
    return random.randint(10000,99999)

#USERS = {
    # this dictionary will hold info of all known system users in format;
    # id: username
#}

#MESSAGES = {
    # this dictionary will hold user messages in format;
    # id: {
    #       "messages":[
    #           {
    #               "sender":username, 
    #               "msg":string, 
    #               "timestamp":time-from--time.asctime()),
    #               "timestamp_in_seconds": time-from-time.time()
    #           },
    #           ...
    #       ],
    #
    #       "last_fetch_time": FLOAT (read from time.time())   
    # }
#}

def login(request):
    
    print request.json
    username = request.json["uname"]
    
    user_found = False
    found_user_id = 0
    users = sms_data.read_user_details(*sms_data.init())
    
    for user in users: 
        if user[1]==username:
            user_found = True
            found_user_id = user[0]
            break
        
    return jencode({"status":user_found, "id":found_user_id})

def register(request):
    login_reply = jdecode(login(request))
    
    if login_reply["status"]:
        return jencode({"status":False, "id":0})
    
    new_id = generate_ID()
    uname = request.json["uname"]
    
    #USERS[new_id] = request.json["uname"]
    #MESSAGES[new_id] = {"messages":[], "last_fetch_time": 0}
    
    db,cur =sms_data.init()
    sms_data.write_user_details(db,cur,new_id,uname)
    
    return jencode({"status":True, "id":new_id})
    
def post_message(request):
    sender_id = request.json["id"]
    
    users = sms_data.read_user_details(*sms_data.init())
    
    sender_in_system = False
    for user in users:
        if user[0]==sender_id:
            sender_in_system = True
            sender_username = user[1]
            break
    
    if not sender_in_system:
        return jencode({"status":False, "log":"sender is unknown"})

    recepients = request.json["recepients"]
    recepients = [int(recepient) for recepient in recepients]
    print recepients
    
    message = request.json["msg"]
    
    log = ""
    db, cur = sms_data.init()
    for recepient in recepients:
        messages = sms_data.save_message(db, cur, recepient, sender_username, message )
        
    print messages
    return jencode({"status":True, "log":log})

def read_inbox(request):
    uid = request.json["id"]
    print uid
    
    #db, cur = sms_data.init()
    messages = sms_data.get_inbox(*sms_data.init() + (uid,))
    
    #if not (uid in messages):
    #    return jencode({"status":False, "messages":[], "log":"unknown client ID"})
    
    return jencode({"status":True, "messages":messages, "log":""})
    
def users_in_system():
    return jencode(sms_data.read_user_details(*sms_data.init()))
    

