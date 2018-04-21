import socket  # Import socket module
import threading
import pickle
import io
import os
import sys
from random import randint
from time2blk import time2blk
from SegTree import *
import time
import datetime
from shard import recvAll, sendAll, msgLength


sendFromPorts  = [randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999)]

updatePort = 4000


script_dir = os.path.dirname(os.path.dirname(__file__))+'/EtherData-master/'

loadFileNum = 50
fileBlockNum = 1000
treeSize = 1000
class slave(threading.Thread):



    def __init__(self, sid, Port,partition,precision):

        self.sid = sid
        self.message = ""
        self.Port = Port

        self.offset = 4000000
        self.host = socket.gethostname()
        self.lock = threading.Lock()
        self.partition = partition
        # create a empty tree
        self.tree = blkSegTree(self.offset, 2000000) # offset (starting blk number), size of the tree
        mapping = time2blk()
        mapping.setBegin(self.offset)
        for i in range(loadFileNum):
            num = self.offset + i * fileBlockNum
            filename = str(num) + '.p'
            with open(script_dir + filename, 'rb') as f:
                blks = pickle.load(f)
                for idx in range(treeSize):
                    self.tree.update(self.getBlock(idx))
                mapping.buildMap(num, filename)

        self.updatePort = updatePort
        self.host = socket.gethostname()
        self.lock = threading.Lock()

        threading.Thread.__init__(self)
        threading.Thread(target=self.listen_new_block, args=()).start()

    def getBlock(self, idx):
        for idx in range(self.sid, fileBlockNum, self.partition):
            self.tree.update(blks[idx])



    def run(self):
        threading.Thread(target=self.listen_new_block, args=()).start()
        self.s = socket.socket()  # Create a socket object
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.Port))  # Bind to the clientPort
        self.s.listen(5)  # Now wait for client connection.
        while True:
            command, addr = self.s.accept()  # Establish connection with client.
            threading.Thread(target=self.on_new_command, args=(command,)).start()



    def on_new_command(self, command,):
        while True:
            msg = recvAll(command, msgLength)
            if (msg != b''):
                file = io.BytesIO(msg)
                while True:
                    try:
                        entry = pickle.load(file)
                        if entry[0] == "query":
                            answer = self.query(entry[1],entry[2])
                            self.sendBack(answer,entry[3])
                    except EOFError:
                        break

    def listen_new_block(self,):
        self.updateSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.updateSocket.bind((self.host, self.updatePort))  # Bind to the clientPort
        self.updateSocket.listen(5)  # Now wait for client connection.
        while True:
            print("here,here,here")
            package, addr = self.updateSocket.accept()  # Establish connection with client.
            threading.Thread(target=self.on_update_block, args=(package,)).start()

    def on_update_block(self,package):
        while True:
            rawblk = recvAll(package)
            blk = pickle.load(io.BytesIO(rawblk))
            print(blk)


    def sendBack(self,answer,toAddr):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, sendFromPorts[self.sid]))
        s.connect(toAddr)
        sendAll(s, pickle.dumps(("answer", answer)), msgLength)
        return 0

    def query(self,start,end,rangeStart=0,rangeEnd=5):
        return self.tree.query_txFee_range(start, end , rangeStart, rangeEnd)


s = slave(0,3333,1,1)
s.start()