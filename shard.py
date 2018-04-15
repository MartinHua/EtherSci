import socket
import threading
from random import randint
from shard_slave import slave
import pickle
import time


slaves = []
slaveNum = 2
precision = 1


slavePorts = [randint(30000, 40000) for _ in range(slaveNum)]
masterPort = randint(26002, 29999)
masterAddr = (socket.gethostname(), masterPort)
listenAddr = (socket.gethostname(), masterPort-1)
print(listenAddr)



def newAddr():
    return (socket.gethostname(), randint(26002, 29999))

def on_new_answer(addr):
    listen = socket.socket()
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen.bind(listenAddr)
    listen.listen(5)
    while True:
        t, addre = listen.accept()
        msg = t.recv(1024)
        print(pickle.loads(msg))

def query(start,end):
    for slave in slaves:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(newAddr())
        s.connect(slave.addr)
        message = pickle.dumps(("query", start, end))
        s.sendall(message)





#start a new slave
for i in range(slaveNum):
    slave  = slave(i, slavePorts[i], slaveNum, precision)
    slaves.append(slave)
    slave.start()

#prepare the listening channel for slaves
threading.Thread(target=on_new_answer, args=(listenAddr,)).start()
time.sleep(0.2)

query(1,2)




