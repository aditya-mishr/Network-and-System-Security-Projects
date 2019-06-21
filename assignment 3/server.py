
import socket
import threading
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto import Random




def wrap_data(public_client,private_server,message,nonce):
    print("nonce----:",nonce)
    encrypted_message=encrypt(public_client,message)
    hash1=SHA512.new(message.encode()).digest()
    hash1=encrypt_hash(private_server,hash1)
    complete_message=encrypted_message + b'$$' + hash1 + b'$$'+ nonce.encode()
    return complete_message

def unwrap_data(private_server,private_client,data):
    data=data.split(b'$$')
    message=decrypt(private_server,data[0])
    hash1=SHA512.new(message).digest()
    hash2=decrypt(private_client,data[1])
    nonce = data[2].decode()
    print("nonce:",nonce)
    if hash1 == hash2:
        global database
        if database.count(message.decode()) > 0:
            print("user verified")
            return "User is registered",nonce
        else:
            return "User is not registered",nonce

def server(private_server,public_client,private_client):
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(3)
    print("...............server is listening...............")
    while True:
        conn, address = server_socket.accept()
        print("server connected to: "+ str(address))
        data=conn.recv(2048)
        data,nonce = unwrap_data(private_server,private_client,data)

        data = wrap_data(public_client,private_server,data,nonce)
        conn.send(data)
        conn.close()


def encrypt(public_key,message):
    public_key = PKCS1_OAEP.new(public_key)
    encrypted_message=public_key.encrypt(message.encode())
    return encrypted_message


def decrypt(private_key,message):
    private_key = PKCS1_OAEP.new(private_key)
    message=private_key.decrypt(message)
    return message


def encrypt_hash(public_key,message):
    public_key = PKCS1_OAEP.new(public_key)
    encrypted_message=public_key.encrypt(message)
    return encrypted_message



def import_private_server():
    f=open('privatekeyserver.pem',"r")
    key = RSA.importKey(f.read())
    f.close()
    return key          # receive response


def import_public_client():
    f=open('publickeyclient.pem',"r")
    key = RSA.importKey(f.read())
    f.close()
    return key          # receive response


def import_private_client():
    f=open('privatekeyclient.pem',"r")
    key = RSA.importKey(f.read())
    f.close()
    return key

if __name__ == '__main__':
    database = []
    filepath = 'db.txt'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            print("{}".format(line.strip()))
            database.append("{}".format(line.strip()))
            line = fp.readline()
            cnt += 1
    
    private_server=import_private_server()
    public_client=import_public_client()
    private_client=import_private_client()
    server(private_server,public_client,private_client)
