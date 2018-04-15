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
import pickle
import time
import datetime

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from time2blk import time2blk
from SegTree import *

slavePort = randint(30000, 40000)
slaveAddress = ('fidelio',slavePort) #('idomeneo',slavePort)#
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


#

data = dict()
mapping = time2blk()
mapping.setBegin(4000000)
for i in range(50):
    num = 4000000 + i*1000
    filename = str(num) +'.p'
    with open('/u/fuli2015/Downloads/EtherData-master/' + filename, 'rb') as f:
        temp = pickle.load(f)
        data.update(temp)
        mapping.buildMap(num, filename)
s = blkSegTree(data, 4000000, p, id, partition) # Partition: number of slaves, ID = slave ID



#query slaves from the start time to the end time
query(1,2)

###############
# build tree
###############
data = dict()
mapping = time2blk()
mapping.setBegin(4000000)
for i in range(50):
    num = 4000000 + i*1000
    filename = str(num) +'.p'
    with open('/u/fuli2015/Downloads/EtherData-master/' + filename, 'rb') as f:
        temp = pickle.load(f)
        data.update(temp)
        mapping.buildMap(num, filename)

s0= blkSegTree(data, 4000000, 1, 0, 2)

s1= blkSegTree(data, 4000000, 1, 1, 2)

###################
#
################
def query(type, start, end):
    low = start/partition
    high = end/partition
    if type == 'query_txFee_range':
        s0.query_txFee_range(low , high + blk, 2, 5) # range from 0.0002-0.0005
        s1.query_txFee_range(low + high, 4000000 + blk, 2, 5)