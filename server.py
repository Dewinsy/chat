# A Server Application That Imports  Custom Module "Logic" That Contains 
# Defined Functions In The Same Folder that facilitates Communication Between Multiple 
# Clients On Remote Locations

IP="0.0.0.0"
PORT=4546
from flask import Flask, request, Response

import logic

app = Flask(__name__)

def reply_to_remote(reply):
	response=Response(reply)
	response.headers["Access-Control-Allow-Origin"]="*"         
	return response

@app.route("/login", methods=["POST"])
def login():
    return reply_to_remote(logic.login(logic.CustomRequest(request)))

@app.route("/register", methods=["POST"])
def register():
    return reply_to_remote(logic.register(logic.CustomRequest(request)))

@app.route("/post_message", methods=["POST"])
def post_mesage():
    return reply_to_remote(logic.post_message(logic.CustomRequest(request)))

@app.route("/read_inbox", methods=["POST"])
def read_inbox():
    return reply_to_remote(logic.read_inbox(logic.CustomRequest(request)))
    
@app.route("/users")
def users_in_system():
    return reply_to_remote(logic.users_in_system())

if __name__ == '__main__':
    app.run(IP,PORT,debug=True)
