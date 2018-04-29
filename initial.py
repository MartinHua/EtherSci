
import socket
import threading
import os
import io
from random import randint
import sys
import pickle
import time


#####################################################################
# change to you local file
# use the following command
#print(os.getcwd())
root_dir = "/u/fuli2015/PycharmProjects/EtherSci/"

############################################################

#begin and offset in slave
begin = 3000000
offset = 3000000

#
treeSize = 6000000
mappingSize = 60000000




counter =int(open(root_dir + "123.txt",'r').readline())

print(counter)
masterPort = counter -1

loadFileNum = 10
fileBlockNum = 1000


slave_num = 10
slaveHosts = ["narsil-"+str(i) for i in range(3, 3+slave_num)]

queryPort = counter
slaveAddrs = [(host, queryPort) for host in slaveHosts]

updatePort = counter+5
slaveUpdateAddrs = [(host, updatePort) for host in slaveHosts]

masterListenFromSlaveAddr = ('rhinoceros-beetle', counter+10)
print(masterListenFromSlaveAddr)

script_dir = '/scratch/cluster/xh3426/etherData/'
#script_dir = os.path.dirname(os.path.dirname(__file__))+'/EtherData-master/'

msgLength = 1024
def recvAll(socket, length=msgLength):
    data = b''
    while True:
        packet = socket.recv(length)
        data += packet
        try:
            pickle.load(io.BytesIO(data))
            return data
        except:
            continue

def sendAll(socket, data, length=msgLength):
    cnt = length
    while cnt < len(data):
        socket.sendall(data[(cnt - length): cnt])
        cnt += length
    socket.sendall(data[(cnt - length): len(data)])


