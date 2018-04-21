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
toStoreTotalBlockNum = fileBlockNum*loadFileNum

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
        self.tree = blkSegTree(self.offset, 100000) # offset (starting blk number), size of the tree
        self.mapping = time2blk(self.offset, 100000)
        #self.mapping.setBegin(self.offset)

        for i in range(loadFileNum):

            filename = str(self.offset) + '.p'
            with open(script_dir + filename, 'rb') as f:
                blks = pickle.load(f)
                #print ('open file', filename, 'check start data', blks[self.offset])
                for idx in range(int(fileBlockNum/self.partition)):

                    self.tree.update(self.getBlock(blks, idx))

                self.mapping.buildMap(self.offset, filename)
            self.offset += fileBlockNum
            #print('current tree size', self.tree.size)

        self.updatePort = updatePort
        self.host = socket.gethostname()
        self.lock = threading.Lock()

        threading.Thread.__init__(self)
        threading.Thread(target=self.listen_new_block, args=()).start()

    def getBlock(self, blks, idx):

        index =  self.sid + self.offset + idx * self.partition
        #print (idx, index, self.offset)
        #print (index, blks[index])
        return blks[index]


    def run(self):
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
        self.updateSocket = socket.socket()
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
            self.tree.update(blk)
            self.mapping.update(blk)
            self.draw()
            print(blk)


    def sendBack(self,answer,toAddr):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, sendFromPorts[self.sid]))
        s.connect(toAddr)
        sendAll(s, pickle.dumps(("answer", answer)), msgLength)
        return 0

    def query(self,start,end,rangeStart=1,rangeEnd=5):
        #return self.tree.query_txFee_range(start, end , rangeStart, rangeEnd)
        return self.tree.query_txFee_Sum(start, end)

    def draw(self):
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
        test = [0] * 31
        pre_b = 0

        for i in range(1, 31):
            t = str(i) + "/07/2017 00:00"
            blk = self.mapping.getBlk(t)
            # print (blk)
            # print (pre_b, blk)
            test[i] = self.query(4000000 + pre_b, 4000000 + blk)
            pre_b = blk

        sns.set_style("darkgrid")
        plt.plot(test[1:30])
        plt.xlabel('days')
        plt.ylabel('Transaction Fees')
        plt.title('Transaction Fees (per block) per day')
        plt.show()

s = slave(0,randint(5000,10000),1,1)
s.start()
print ('test', s.query(4000000, 4000100))


# # test--- get transactopn fees per hour for 12/07/2017
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# test = [0]*24
# pre_b = 0
#
# for i in range(24):
#     t = "12/07/2017 " + str(i) + ":00"
#     blk = s.mapping.getBlk(t)
#     #print (blk)
#     #print (pre_b, blk)
#     test[i] = s.query(4000000+ pre_b, 4000000 + blk)
#     pre_b = blk
#
#
# sns.set_style("darkgrid")
# plt.plot(test[1:24])
# plt.xlabel('Hours')
# plt.ylabel('Transaction Fees')
# plt.title('Transaction Fees (per block) per hour')
# plt.show()

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
test = [0] * 31
pre_b = 0

for i in range(1, 31):
    t = str(i) + "/07/2017 00:00"
    blk = s.mapping.getBlk(t)
    # print (blk)
    # print (pre_b, blk)
    test[i] = s.query(4000000 + pre_b, 4000000 + blk)
    pre_b = blk

sns.set_style("darkgrid")
plt.plot(test[1:30])
plt.xlabel('days')
plt.ylabel('Transaction Fees')
plt.title('Transaction Fees (per block) per day')
plt.show()

