# https://www.youtube.com/watch?v=3QiPPX-KeSc&ab_channel=TechWithTim
import socket
import threading

# HEADER is a fixed length in bytes
# it should be the first msg sent by a client to determine the length of the incoming msg
# for example: if the msg the client wants to send is of length 5 bytes, HEADER value will be 5 padded to 64 bytes
HEADER = 64
PORT = 5050
# returns the IPv4 address of the machine
# can also use cmd, type ipconfig and copy the IPv4 address
# using this IP will run the socket locally
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected...\n')
    connected = True
    while connected:
        # decide how many bytes you want to accept
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f'[{addr}] {msg}')
    conn.close()


def start():
    server.listen()
    print(f'LISTENING Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() -1}')


print('[STARTING] server is starting...')
start()
