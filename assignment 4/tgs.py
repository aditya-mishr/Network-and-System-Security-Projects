import datetime
import pyaes
import string
import random
import socket
import base64

def randomString(stringLength=32):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def encrypt(key, msg):
    # A 256 bit (32 byte) key
    key = key.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(key)    
    ciphertext = aes.encrypt(msg)
    return ciphertext

def decrypt(key,ciphertext):
    key = key.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(key)
    # decrypted data is always binary, need to decode to plaintext
    decrypted = aes.decrypt(ciphertext).decode('utf-8')
    return decrypted

def process_data(data):
    data=data.split("$$")
    id_v = data[0]
    ticket_cipher = data[1]
    #authenticator = data[2]

    key_tgs = "12345678912345678912345678912345"
    ticket_tgs = decrypt(key_tgs,base64.b64decode(ticket_cipher))
    ticket = ticket_tgs.split("$$")

    K_c_tgs = ticket[0]
    ID_C = ticket[1]
    print(ID_C)

    K_v = "12345678912345678912345678912345"
    K_c_v = randomString()
    TS4 = str(datetime.datetime.now())
    Lt4 = "334445"
    
    ticket_v = K_c_v  + "$$" + ID_C  + "$$"  + id_v  + "$$" + TS4 + "$$" + Lt4
    
    ticket_v_cipher = encrypt(K_v,ticket_v)
    
    
    res = K_c_v + "$$" + id_v + "$$" + TS4 + "$$" + str(base64.b64encode(ticket_v_cipher),'utf-8')
    res_cipher = encrypt(K_c_tgs,res)
    return res_cipher 

def server():

    host = socket.gethostname()
    port = 6000

    server_socket = socket.socket()
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(3)
    print("...............server is listening...............")
    
    conn, address = server_socket.accept()
    print("server connected to: "+ str(address))
    data=conn.recv(2048).decode()
    res = process_data(data)
    conn.send(res)
    conn.close()

if __name__ == '__main__':
    server()
