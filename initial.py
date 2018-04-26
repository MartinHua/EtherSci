
import io
import pickle
import socket
import os
from random import randint

masterListenPort = randint(26002, 29999)
# masterAddr = (socket.gethostname(), masterPort)
listenAddr = (socket.gethostname(), masterListenPort)


slave_num = 10
hosts  = ["narsil-"+str(i) for i in range (3,3+slave_num)]
slaveAddrs = [(host,5000) for host in hosts]


updatePort = 4000


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