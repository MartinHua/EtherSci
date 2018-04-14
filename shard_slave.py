import socket  # Import socket module
import threading
import pickle
import io
import sys
from random import randint
import time
import datetime

msgLength = 1024

def recvAll(socket, length):
    data = b''
    while True:
        packet = socket.recv(length)
        data += packet
        if len(packet) < length:
            return data

def sendAll(socket, data, length):
    cnt = length
    while cnt < len(data):
        socket.sendall(data[(cnt - length): cnt])
        cnt += length
    socket.sendall(data[(cnt - length): cnt])


sendFromPorts  = [randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999)]



class slave(threading.Thread):

    def __init__(self, sid, Port):
        self.sid = sid
        self.message = ""
        self.Port = Port

        self.host = socket.gethostname()
        self.lock = threading.Lock()

        threading.Thread.__init__(self)


    def run(self):

        self.s = socket.socket()  # Create a socket object
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.Port))  # Bind to the clientPort
        self.s.listen(5)  # Now wait for client connection.
        while True:
            command, addr = self.s.accept()  # Establish connection with client.
            threading.Thread(target=self.on_new_command, args=(command, addr)).start()



    def on_new_command(self, command, addr):
        while True:
            msg = recvAll(command, msgLength)
            if (msg != b''):
                file = io.BytesIO(msg)
                while True:
                    try:
                        entry = pickle.load(file)
                        if entry[0] == "query":
                            answer = self.query(entry[1],entry[2])
                            self.sendBack(answer,addr)
                    except EOFError:
                        break


    def sendBack(self,answer,toAddr):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, sendFromPorts[self.sid]))
        s.connect((toAddr[0],toAddr[1]-1))
        sendAll(s, pickle.dumps(("answer", answer)), msgLength)
        return 0

    def query(self,start,end):
        return 299
