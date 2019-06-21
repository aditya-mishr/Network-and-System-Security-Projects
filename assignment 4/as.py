
import socket
import random
import string
import datetime
from aes import encryption , decryption
import base64


def randomString(stringLength=32):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


client_key = "12345678912345678912345678912345"
tgt_key = "12345678912345678912345678912345"

def server():

    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(3)
    print("...............server is listening...............")
  
    conn, address = server_socket.accept()
    print("server connected to: "+ str(address))
    data=conn.recv(2048).decode()
    data = data.split("$$")
    id_client = data[0]
    id_tgt = data[1]
    time = str(datetime.datetime.now())
    key = randomString()
    print(key)
    ticket = key + "$$" + id_client + "$$" + id_tgt + "$$" + time
    ticket = encryption(tgt_key,ticket)
    print(ticket)
    message = key + "$$" + id_tgt + "$$" + time + "$$" + str(base64.b64encode(ticket),'utf-8')
    message = encryption(client_key , message)
    conn.send(message)
    conn.close()



if __name__ == '__main__':
    server()
