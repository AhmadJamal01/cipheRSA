import socket
import threading # for multithreading

HEADER = 64 # bytes to send
FORMAT = 'utf-8'
PORT = 5050 
DISCONNECT_MESSAGE = "bye!"
SERVER = socket.gethostbyname(socket.gethostname()) # returns the IPv4 address of the machine , in order to avoid hard coded IPV4
ADDR = (SERVER, PORT) # Bind socket to specific address
client = socket.socket(
     socket.AF_INET, # IPv4 , AF_INET is the address family
     socket.SOCK_STREAM # SOCK_STREAM is the type of socket
     )
print("[CONNECTING] to server...")
client.connect(ADDR) # connect to the server
# print the server info
print(f'[CONNECTED] to {client.getsockname()}')
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

SENDING = True
while SENDING:
    msg = input("Enter a message: ")
    send(msg)
    if msg == DISCONNECT_MESSAGE:
        SENDING = False
