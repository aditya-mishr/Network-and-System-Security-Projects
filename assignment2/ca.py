
import socket
import datetime



def encrypt_rsa(m,key):
    [e,n]=key
    if e==1:
        return m % n
    elif e%2==1 :
        return ((encrypt_rsa(m,(int(e/2),n)) ** 2)* m)%n
    else :
        return (encrypt_rsa(m,(int(e/2),n)) ** 2)%n


def encrypt(data,private_key):
    new_data=[]
    for d in data:
        new_data.append(encrypt_rsa(d,private_key))
    return new_data



def server_program(certificate):
    private_key=[23,187]
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(2)
    print("...............server is listening...............")
    while True:
        conn, address = server_socket.accept()
        print("server connected to: "+ str(address))
        data = conn.recv(1024)#.decode()
        print("data received:",data)
        now=datetime.datetime.now()
        hour=now.hour
        minute=now.minute
        #print("request from client:"+data.decode())
        if data.decode() == "2":
            #print(certificate[0])
            certificate[1].append(hour)
            certificate[1].append(minute)
            certi=encrypt(certificate[1],private_key)
            print("encrypt certificate:" ,certi)
            conn.send(bytes(certi))
        else:
            #print(certificate[1])
            certificate[0].append(hour)
            certificate[0].append(minute)
            certi=encrypt(certificate[0],private_key)
            print("encrypt certificate:",certi)
            conn.send(bytes(certi))
        print("connection close")

        conn.close()  # close the connection


if __name__ == '__main__':
    certificate = [[1,5,119],[2,35,119]]
    server_program(certificate)
