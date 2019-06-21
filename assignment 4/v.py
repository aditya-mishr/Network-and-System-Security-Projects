
import socket
import random
import string
import datetime
from aes import encryption , decryption
import base64

server_key = "12345678912345678912345678912345"
#tgt_key = "12345678912345678912345678912345"

def server():

    host = socket.gethostname()
    port = 7000

    server_socket = socket.socket()
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(3)
    print("...............server is listening...............")
    while True:
        conn, address = server_socket.accept()
        print("server connected to: "+ str(address))
        data=conn.recv(2048).decode()
        data = data.split("$$")
        ticket = data[0]
        autheticator = data[1]
        ticket = decryption(server_key,base64.b64decode(ticket))
        ticket = ticket.split("$$")
        key_c_v = ticket[0]

        time = decryption(key_c_v , base64.b64decode(autheticator)).split("$$")
        print(time)
        message = encryption(key_c_v,time[-1])
        conn.send(message)
        conn.close()



if __name__ == '__main__':
    server()
