import socket
import threading
import argparse
import time 

lock = threading.Lock()

def act_as_server(host, port):
    print("I am a server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket binded to :" + host + " : " + str(port) )
    s.listen(5)
    while True :
        conn, addr = s.accept()
        lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        thread = threading.Thread(target=receive_data, args=(conn, ))
        thread.start()

def receive_data(conn) :
    recieved_data = conn.recv(1024)
    print("Recieved :" + str(recieved_data.decode("ascii")))
    lock.release()
    conn.send("recieved".encode("ascii"))
    conn.close()

def send_data(host, port) :
    dataToSend = 0
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print("Connected to :" + host + " : " + str(port) )
        print("Send data ->" + str(dataToSend) )
        s.send(str(dataToSend).encode('ascii'))
        print("Recieved :" + str(s.recv(1024).decode("ascii")))
        dataToSend = dataToSend + 1
        time.sleep(5)
    s.close()

def Main() :
    host = "127.0.0.1"
    c_port = 12345
    s_port = 12346
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--opmode', help='s or c', required=True)
    args = args_parser.parse_args()
    opMode = args.opmode
    
    act_as_client(host, c_port)
    act_as_server(host, s_port)

def act_as_client(host, port):
    print("I am a client")
    thread = threading.Thread(target=send_data, args=(host, port))
    thread.start()



if __name__ == '__main__':
    Main()

    


