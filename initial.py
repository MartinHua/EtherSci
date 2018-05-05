
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
root_dir = "/u/xh3426/cs380D/EtherSci/"

############################################################


counter =int(open(root_dir + "123.txt", 'r').readline())
# begin and offset in slave
begin = 3000000
offset = 3000000

#
treeSize = 1200000
mappingSize = 1200000


print(counter)
masterPort = counter - 1

loadFileNum = 1000
fileBlockNum = 1000


slave_num = 10
slaveId = [3, 4, 5, 6, 7, 8, 10, 11, 12, 13]
slaveHosts = ["narsil-"+str(i) for i in slaveId]

queryPort = counter
slaveAddrs = [(host, queryPort) for host in slaveHosts]

updatePort = counter+5
slaveUpdateAddrs = [(host, updatePort) for host in slaveHosts]

masterHost = 'narsil-2'
masterListenFromSlaveAddr = (masterHost, counter+10)
print(masterListenFromSlaveAddr)

print((masterHost, masterPort))
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


