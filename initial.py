
import io
import pickle
import socket
import os
from random import randint

masterListenPort = randint(26002, 29999)
# masterAddr = (socket.gethostname(), masterPort)
listenAddr = (socket.gethostname(), masterListenPort)


slave_num = 10
slaveHosts = ["narsil-"+str(i) for i in range(3, 3+slave_num)]

queryPort = 5000
slaveAddrs = [(host, queryPort) for host in slaveHosts]

updatePort = 4000
slaveUpdateAddrs = [(host, updatePort) for host in slaveHosts]


script_dir = '/scratch/cluster/xh3426/etherData/'

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