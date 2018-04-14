import socket
import threading

from random import randint
from shard_slave import slave
from shard_master import master
import time
from ctypes import c_int, addressof
import pickle
import sys
import os


slavePort = randint(30000, 40000)
slaveAddress = ('idomeneo',slavePort)#('fidelio',slavePort)
masterPort = randint(26002, 29999)
masterAddr = (socket.gethostname(), masterPort)
listenAddr = (socket.gethostname(), masterPort-1)
print(listenAddr)

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
    s = socket.socket()
    addr = (socket.gethostname(), slavePort)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(masterAddr)
    s.connect(slaveAddress)
    message = pickle.dumps(("query", start, end))
    s.sendall(message)


#start a new slave
slave = slave(0, slavePort)
slave.start()
time.sleep(0.5)

#prepare the listening channel for slaves
threading.Thread(target=on_new_answer, args=(listenAddr,)).start()
time.sleep(0.2)


#query slaves from the start time to the end time
query(1,2)


