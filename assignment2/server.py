
import socket
import threading

client1=[]
client2=[]

def recev(c,n):
    while True:
        data=c.recv(1024)
        if str(n[1])=="7000":
            #print("client1")
            client1.append(list(data))
        else:
            #print("client2")
            client2.append(list(data))
def sendd(c,n):
    while True:
        if str(n[1])=="7000":
            if len(client2)>0:
                c.send(bytes(client2.pop(0)))
        else:
            if len(client1)>0:
                c.send(bytes(client1.pop(0)))

def server_program():
    host = socket.gethostname()
    port = 6000

    server_socket = socket.socket()
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(3)
    print("...............server is listening...............")
    while True:
        conn, address = server_socket.accept()
        print("server connected to: "+ str(address))
        thread1=threading.Thread(target=recev,args=(conn,address))
        thread1.daemon= True
        thread1.start()
        thread2=threading.Thread(target=sendd,args=(conn,address))
        thread2.daemon=True
        thread2.start()

        #conn.close()  # close the connection


if __name__ == '__main__':

    server_program()
