from initial import masterPort,recvAll
import socket
import threading
import pickle
from random import randint
import io

Port =  randint(3000, 9000)
def query(s,start,end):
    msg = pickle.dumps(("query",start,end))
    s.sendall(msg)

def parse(msg):
    if (msg != b''):
        file = io.BytesIO(msg)
        while True:
            try:
                entry = pickle.load(file)
                return entry
            except EOFError:
                break


masterAddr = (socket.gethostname(),masterPort)

s=socket.socket()
s.bind((socket.gethostname(), Port))
s.connect(masterAddr)

test = [0] * 24
pre_t = "12/07/2017 0:00"

for i in range(1, 24):
    t = "12/07/2017 " + str(i) + ":00"
    query(s,pre_t, t)
    test[i] = parse(recvAll(s))
    print(test[i], 'query from', pre_t, ' to ', t)
    pre_t = t
from draw import *

draw(test[1:])

