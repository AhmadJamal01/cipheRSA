from flask import Flask , request, jsonify ,session
from helpers import *
from flask_socketio import SocketIO, emit , join_room
from collections import deque
import json
from ast import literal_eval
channelsCreated = []
# Keep track of users logged (Check for username)
usersLogged = []
# Instanciate a dict
channelsMessages = dict()

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*",async_mode='eventlet')
app.config["SECRET_KEY"] = "my secret key"

@app.route('/signup' , methods=['POST'])
def signup():
    data = request.get_json()
    print(data)
    p = data['p']
    q = data['q']
    e = data['e']
    errorMsg = ""
    if p != "":
        p = int(data['p'])
    else:
        p= generatePrime(256)
    if q != "":
        q = int(data['q'])
    else:
        q = generatePrime(256)
        while p==q:
            q = generatePrime(256)
    if e != "":
        e = int(data['e'])
    else:
        e = random.randrange(1,(p-1)*(q-1))
        while not testexponent(e,p,q):
            e = random.randrange(1,(p-1)*(q-1))
    username = data['username']
    d= 0
    ptest=fermatPrimalityTest(p)
    qtest=fermatPrimalityTest(q)
    etest=testexponent(e,p,q)
    d  = getPrivateKey(e,p,q)
    if not etest :
        errorMsg += "e is not valid"
    if  not ptest :
        errorMsg = "p is not prime "
    if not qtest :
        errorMsg += "q is not prime "
    
    if etest and ptest and qtest :
        user_data = {
            "username":username,
            "n" : p*q,
            "e" : e,
        }
        json_object = json.dumps(user_data, indent = 4)
        if username == "jemy" :
            with open("jemy.json", "w") as outfile:
                outfile.write(json_object)
        else:
            with open("ihab.json", "w") as outfile:
                outfile.write(json_object)
            
    print(jsonify({'Error':errorMsg , 'privateKey':d , 'publicKey':e , 'n' : p*q}))
    return jsonify({'Error':errorMsg , 'privateKey':d , 'publicKey':e , 'n' : p*q})

@app.route("/obtainpublic", methods=['GET'])
def obtainpublic():
    data = request.get_json()
    if data['username'] == "jemy" :
        with open('ihab.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
    else:
        with open('jemy.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)

    return jsonify(json_object)

       
@app.route("/sendmsg", methods=['POST'])
def sendmsg():
    data = request.get_json()
    if (data["username"]=="jemy"):
        with open('ihab.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        n = json_object["n"]
        m_encrypted=use_encrypt(data["message"],json_object["e"],n)
        f = open("ihabroomview.txt", "a")
        f.write(data["username"]+" "+str(m_encrypted) + "\n")
        f2 = open("jemyroomview.txt", "a")
        f2.write(data["username"]+" "+str(data["message"]) + "\n")
    else:
        with open('jemy.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        n = json_object["n"]
        m_encrypted=use_encrypt(data["message"],json_object["e"],n)
        f = open("jemyroomview.txt", "a")
        f.write(data["username"]+" "+str(m_encrypted) + "\n")
        f2 = open("ihabroomview.txt", "a")
        f2.write(data["username"]+" "+str(data["message"]) + "\n")
    f = open("chatroom.txt", "a")
    f.write(data["username"]+" "+str(data["message"])+" "+str(m_encrypted) + "\n")
    return jsonify({'Error':"",'message':data["message"]})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    d = int(data["d"])
    p = int(data["p"])
    q = int(data["q"])
    n = int(data["N"])
    print(literal_eval(data["message"]))
    print(d)
    print(p)
    print(q)
    m = use_decrypt(literal_eval(data["message"]),d,p,q)
    print(m);
    return jsonify({'Error':"",'message':m})


@socketio.on('jemysevent')
def send_msg():
    with open('jemyroomview.txt', 'r') as openfile:
        lines = openfile.read().splitlines()
    emit('jemymessage', {
        'yourmsgs': lines
        }, broadcast=True)
    

@socketio.on('ihabsevent')
def send_msg():
    with open('ihabroomview.txt', 'r') as openfile:
        lines = openfile.read().splitlines()
    emit('ihabmessage', {
        'yourmsgs': lines}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)