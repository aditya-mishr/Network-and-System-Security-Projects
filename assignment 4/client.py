import socket
import datetime
import numpy as np
from aes import encryption , decryption
import base64

client_key = "12345678912345678912345678912345"

def connect_to_as():

    host = socket.gethostname()
    port = 5000 #server port
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("...............connection established................")

    id_client = "1"
    id_tgt = "3"
    time  =  datetime.datetime.now()
    message = id_client + "$$" + id_tgt + "$$" + str(time)
    message = message.encode()
    client_socket.send(message)
    data = client_socket.recv(2024)
    data = decryption(client_key , data)
    data = data.split("$$")
    key_c_tgs = data[0]
    print(key_c_tgs)
    ticket = data[-1]
    print(ticket)
    return key_c_tgs , ticket

def connect_to_tgs(key_c_tgs, ticket):
    host = socket.gethostname()
    port = 6000 #server port
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("...............connection established................")

    id_client = "1"
    id_server = "4"
    ts3  =  datetime.datetime.now()

    #create authenticator
    auth = encryption(key_c_tgs,id_client + "$$" + str(ts3) )
    message = id_server + "$$" + ticket + "$$" + str(auth)
    message = message.encode()
    client_socket.send(message)
    data = client_socket.recv(2024)

    data = decryption(key_c_tgs , data)
    data = data.split("$$")
    key_c_v = data[0]
    print(key_c_v)
    ticket_v = data[-1]
    print(ticket_v)
    return key_c_v,ticket_v

def make_authenticator(key):
    id_client = "1"
    time = str(datetime.datetime.now())
    message = id_client + "$$" + time
    return encryption(key,message) , time


def connect_to_v(key_c_v , ticket):

    host = socket.gethostname()
    port = 7000 #server port
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("...............connection established................")

    authenticator ,time1 = make_authenticator(key_c_v)
    authenticator = str(base64.b64encode(authenticator),"utf-8")
    message = ticket + "$$" + authenticator
    client_socket.send(message.encode())
    data = client_socket.recv(2024)
    time2 = decryption(key_c_v, data)
    print("hey:",time1)
    print(time2)
    if time1 == time2:
        print("connected to right server")

if __name__ == '__main__':

    key_c_tgs, ticket =connect_to_as()
    key_c_v,ticket_v = connect_to_tgs(key_c_tgs, ticket)
    connect_to_v(key_c_v,ticket_v)
