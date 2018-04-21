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

listenPort = randint(30000, 40000)
# slaveAddress = ('fidelio',slavePort) #('idomeneo',slavePort)#
masterListenPort = randint(26002, 29999)
# masterAddr = (socket.gethostname(), masterPort)
listenAddr = (socket.gethostname(), masterListenPort)
host = socket.gethostname()
msgLength = 1024
def recvAll(socket, length=msgLength):
    data = b''
    while True:
        packet = socket.recv(length)
        data += packet
        try:
            pickle.loads(data)
            return data
        except:
            continue

def sendAll(socket, data, length=msgLength):
    cnt = length
    while cnt < len(data):
        socket.sendall(data[(cnt - length): cnt])
        cnt += length
    socket.sendall(data[(cnt - length): len(data)])


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

def query(start,end,offset):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, randint(30000, 40000)))
    s.connect((host, listenPort+offset))
    message = pickle.dumps(("query", start, end,listenAddr))
    s.sendall(message)

#
# #start a new slave
# slave = slave(0, slavePort)
# slave.start()
# time.sleep(0.5)
#
# #prepare the listening channel for slaves
# threading.Thread(target=on_new_answer, args=(listenAddr,)).start()
# time.sleep(0.2)
#
#
# #
#
# data = dict()
# mapping = time2blk()
# mapping.setBegin(4000000)
# for i in range(50):
#     num = 4000000 + i*1000
#     filename = str(num) +'.p'
#     with open('/u/cchsu/Downloads/EtherData-master/' + filename, 'rb') as f:
#         temp = pickle.load(f)
#         data.update(temp)
#         mapping.buildMap(num, filename)
# s = blkSegTree(data, 4000000, p, id, partition) # Partition: number of slaves, ID = slave ID
#
#
#
# #query slaves from the start time to the end time
# query(1,2)

###############
# build tree
###############
# data = dict()
# mapping = time2blk()
# mapping.setBegin(4000000)
# for i in range(1):
#     num = 4000000 + i*1000
#     filename = str(num) +'.p'
#     with open('/u/fuli2015/Downloads/EtherData-master/' + filename, 'rb') as f:
#         temp = pickle.load(f)
#         data.update(temp)
#         mapping.buildMap(num, filename)
#
# # 2 partition
# s0= blkSegTree(data, 4000000, 1, 0, 2)
# s1= blkSegTree(data, 4000000, 1, 1, 2)

# 1 partition
#s0 = blkSegTree(data, 4000000, 1, 0, 1)


###################
#
################
# def query(type, start, end):
#     partition = 2
#     low = start
#     high = start + int((end - start)/partition)
#     print (low, high)
#     if type == 'query_txFee_range':
#         ans = 0
#         #ans += s0.query_txFee_Num(low,high)
#         #ans += s1.query_txFee_Num(low, high)
#         ans += s0.query_txFee_range(low, high, 1, 9)
#         ans += s1.query_txFee_range(low, high, 1, 9)
#         #s1.inorder(s1.root)
#         print (ans)
s0 = slave(0,listenPort,  2,1)
s0.start()
s1 = slave(1,listenPort+1,2,1)
s1.start()


#prepare the listening channel for slaves
threading.Thread(target=on_new_answer, args=(listenAddr,)).start()
time.sleep(0.2)


query(4000000,4000999,0)
query(4000000,4000999,1)
# query(2,5,1)
#query('query_txFee_range', 4000000, 4000999)