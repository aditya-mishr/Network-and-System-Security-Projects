import socket
import time
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto import Random
import numpy as np


def wrap_data(public_server,private_client,message,nonce):
    encrypted_message=encrypt(public_server,message)
    hash1=SHA512.new(message.encode()).digest()
    hash1=encrypt_hash(private_client,hash1)
    complete_message=encrypted_message + b'$$' + hash1 + b'$$'+ nonce.encode()
    return complete_message


def unwrap_data(private_client,private_server,data,nonce_1):
        data=data.split(b'$$')
        message=decrypt(private_client,data[0])
        hash1=SHA512.new(message).digest()
        hash2=decrypt(private_server,data[1])
        nonce = data[2]
        if hash1 == hash2 and nonce.decode()==nonce_1:
            print("data from correct server,nonce:",nonce.decode())
            return message
        else:
            return "data from wrong server"


def connect(private_client,public_server,private_server):

    host = socket.gethostname()
    port = 5000 #server port

    nonce = np.random.randint(1,10000)
    nonce = str(nonce)
    print("nonce:",nonce)
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("...............connection established................")
    message = input("enter the date of birth to varify in formate(dd-mm-yyyy) :")
    complete_message = wrap_data(public_server,private_client,message,nonce)
    client_socket.send(complete_message)
    data = client_socket.recv(2024)
    data = unwrap_data(private_client,private_server,data,nonce)
    print(data.decode())



def encrypt_hash(public_key,message):
    public_key = PKCS1_OAEP.new(public_key)
    encrypted_message=public_key.encrypt(message)
    return encrypted_message


def encrypt(public_key,message):
    public_key = PKCS1_OAEP.new(public_key)
    encrypted_message=public_key.encrypt(message.encode())
    return encrypted_message


def decrypt(private_key,message):
    private_key = PKCS1_OAEP.new(private_key)
    message=private_key.decrypt(message)
    return message



def import_private_client():
    f=open('privatekeyclient.pem',"r")
    key = RSA.importKey(f.read())
    f.close()
    return key


def import_private_server():
    f=open('privatekeyserver.pem',"r")
    key = RSA.importKey(f.read())
    f.close()
    return key


def import_public_server():
    f=open('publickeyserver.pem',"r")
    key = RSA.importKey(f.read())
    f.close()
    return key


if __name__ == '__main__':
    private_client=import_private_client()
    public_server=import_public_server()
    private_server=import_private_server()
    connect(private_client,public_server,private_server)
