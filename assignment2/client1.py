import socket
import time
import threading

def encrypt_rsa(m,key):
    [e,n]=key
    if e==1:
        return m % n
    elif e%2==1 :
        return ((encrypt_rsa(m,(int(e/2),n)) ** 2)* m)%n
    else :
        return (encrypt_rsa(m,(int(e/2),n)) ** 2)%n

def decrypt_rsa(m,key):
    [d,n]=key
    if d==1:
        return m % n
    elif d%2 ==1:
        return ((decrypt_rsa(m,(int(d/2),n))**2)*m)% n
    else:
        return (decrypt_rsa(m,(int(d/2),n))**2)% n

def encrypt(data,private_key):
    new_data=[]
    for d in data:
        new_data.append(encrypt_rsa(d,private_key))
    return new_data


def decrypt(data,public_key):
    new_data=[]
    for d in data:
        new_data.append(decrypt_rsa(d,public_key))
    return new_data


def get_public_key_client2():
    host = socket.gethostname()
    port = 5000 #server port
    public_key=[7,187]
    client_port=3000

    client_socket = socket.socket()  # instantiate
    client_socket.bind((host,client_port))
    client_socket.connect((host, port))  # connect to the server
    print("...............connection established................")

    client_socket.send("2".encode())  # send message
    data = client_socket.recv(1024)  # receive response
    data=list(data)
    data=decrypt(data,public_key)
    print("...............public key received...............")
    client_socket.close()  # close the connection
    print("...............connection closed.................")
    return data

def recev(s,public_key,private_key):
    m=0
    while True:
        data=s.recv(1024)
        data=list(data)
        data=decrypt(data,public_key)
        data=[c+40 for c in data]
        data=[chr(c) for c in data]
        data="".join(data)
        print("client 2 :"+data)
        if data[:3] != "ack":
            m=m+1
            ack="ack"+str(m)
            ack=[ord(c) for c in ack]
            ack=[c-40 for c in ack]
            ack=encrypt(ack,private_key)
            s.send(bytes(ack))



def connect(private_key,public_key):
    host = socket.gethostname()
    port = 6000 #server port

    client_port=7000

    client_socket = socket.socket()  # instantiate
    client_socket.bind((host,client_port))
    client_socket.connect((host, port))  # connect to the server
    print("...............connection established................")
    thread1=threading.Thread(target=recev,args=(client_socket,public_key,private_key))
    thread1.daemon= True
    thread1.start()

    while True:
        data=input("")
        #print("client1:" + data)
        data=[ord(c) for c in data]
        data=[c-40 for c in data]
        data=encrypt(data,private_key)
        client_socket.send(bytes(data))





if __name__ == '__main__':
    private_key = [77,119]

    certificate= get_public_key_client2()
    cer={"ID":certificate[0] , "Public key":[certificate[1],certificate[2]],"Time":str(certificate[3])+":"+str(certificate[4])}
    print(cer)
    public_key=[certificate[1],certificate[2]]
    #print(public_key)
    connect(private_key,public_key)
