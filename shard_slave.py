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



class slave(threading.Thread):

    def __init__(self, sid, Port,partition,precision):

        self.sid = sid
        self.message = ""
        self.Port = Port
        self.updatePort = updatePort

        self.host = socket.gethostname()
        self.lock = threading.Lock()
        data = dict()
        # mapping = time2blk()
        # mapping.setBegin(4000000)
        # for i in range(50):
        #     num = 4000000 + i * 1000
        #     filename = str(num) + '.p'
        #     with open(script_dir + filename, 'rb') as f:
        #         temp = pickle.load(f)
        #         data.update(temp)
        #         mapping.buildMap(num, filename)

        # self.tree = blkSegTree(data, 4000000, precision, sid, partition)
        threading.Thread.__init__(self)



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
        self.s = socket.socket()  # Create a socket object
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.updatePort))  # Bind to the clientPort
        self.s.listen(5)  # Now wait for client connection.
        while True:
            print("here")
            packageBlk, addr = self.s.accept()  # Establish connection with client.
            rawblk = recvAll(packageBlk)
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