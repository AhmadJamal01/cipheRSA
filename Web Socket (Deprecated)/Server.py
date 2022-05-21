import socket
import threading # for multithreading

HEADER = 64 # bytes to send
FORMAT = 'utf-8'
PORT = 5050 
DISCONNECT_MESSAGE = "bye!"
SERVER = socket.gethostbyname(socket.gethostname()) # returns the IPv4 address of the machine , in order to avoid hard coded IPV4
ADDR = (SERVER, PORT) # Bind socket to specific address
server = socket.socket(
     socket.AF_INET, # IPv4 , AF_INET is the address family
     socket.SOCK_STREAM # SOCK_STREAM is the type of socket
     )

server.bind(ADDR) # bind the socket to the address

def handle_client(conn,addr):
    print(f'[NEW CONNECTION] {addr} connected...')
    connected = True
    while connected:
        # decide how many bytes you want to accept
        msg_length = conn.recv(HEADER).decode(FORMAT) # receive the length of the incoming msg (blocking we will not pass this line untill we receive a msg)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f'[DISCONNECTED] {addr} disconnected...')
            print(f'[{addr}] {msg}')
    conn.close()

def start():
    server.listen()
    print(f'[STARTING] server is starting...')
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        # when a new connection occures, accept it and pass it to the handle_client function
        # and store the address of the client in the variable addr
        # and store object of the client in the variable conn to be used in the handle_client function
        conn, addr = server.accept() # wait for a connection (blocking) , accept the connection
        # create a new thread to handle the client
        # we subtract 1 from the threading.active_count() because the main thread is also a thread and it's running 
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() -1}') # print the number of active threads (connections)
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # create a new thread to handle the client
        thread.start() # start the thread


