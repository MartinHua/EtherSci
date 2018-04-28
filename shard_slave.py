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
from initial import recvAll, sendAll, msgLength




sendFromPorts  = [randint(2602,29999)]*10

updatePort = 4000


script_dir = os.path.dirname(os.path.dirname(__file__))+'/EtherData-master/'

loadFileNum = 30
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
        self.begin = 4000000
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
            print ('update')
            rawblk = recvAll(package)
            blk = pickle.load(io.BytesIO(rawblk))

            self.tree.update(blk)

            self.mapping.update(blk)

            self.draw_min()

            #print(blk)


    def sendBack(self,answer,toAddr):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, sendFromPorts[self.sid]))
        s.connect(toAddr)
        sendAll(s, pickle.dumps(("answer", answer)), msgLength)
        return 0

    def query(self,startTime, endTime):
        #return self.tree.query_txFee_range(start, end , rangeStart, rangeEnd)
        start = int(self.mapping.getBlk(startTime) / self.partition)
        end = int(self.mapping.getBlk(endTime) / self.partition)

        return self.tree.query_txFee_Sum(self.begin + start, self.begin + end)
        # return self.tree.query_topK_addrs(self.begin + start, self.begin + end)
        # return self.tree.query_topK_pairs(self.begin + start, self.begin + end)

    def draw_day(self):
        import matplotlib.pyplot as plt
        import numpy as np50
        import seaborn as sns
        test = [0] * 31
        pre_b = 0
        print('-----------------------------------------------------------')
        for i in range(1, 20):
            t = str(i) + "/07/2017 00:00"
            blk = self.mapping.getBlk(t)
            # print (blk)
            # print (pre_b, blk)
            test[i] = self.query(4000000 + pre_b, 4000000 + blk)
            pre_b = blk
            print(test[i], 'query from', 4000000 + pre_b, ' to ', 4000000 + blk)
        print('-----------------------------------------------------------')
        sns.set_style("darkgrid")
        plt.plot(test[2:])
        plt.xlabel('days')
        plt.ylabel('Transaction Fees')
        plt.title('Transaction Fees (per block) per day')
        plt.show()
    def draw_hr(self):

        # test--- get transactopn fees per hour for 12/07/2017
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
        test = [0]*24
        pre_b = 0

        for i in range(1, 24):
            t = "16/07/2017 " + str(i) +':00'
            blk = self.mapping.getBlk(t)

            print (pre_b, blk)
            test[i] = (self.query(4000000 + pre_b, 4000000 + blk)) / 10 ** 9
            pre_b = blk

        print (' [draw] ', test[2:])
        sns.set_style("darkgrid")
        plt.plot(test[2:])
        plt.xlabel('Hours')
        plt.ylabel('Transaction Fees')
        plt.title('Transaction Fees (per block) per hour')
        plt.show()
    def draw_min(self):

        # test--- get transactopn fees per hour for 12/07/2017
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
        test = [0]*60
        pre_b = 0

        for i in range(1,60):
            t = "16/07/2017 6:" + str(i)
            blk = self.mapping.getBlk(t)

            print (pre_b, blk)
            test[i] = (self.query(4000000 + pre_b, 4000000 + blk)) / 10 ** 9
            pre_b = blk

        print (' [draw] ', test[2:])
        sns.set_style("darkgrid")
        plt.plot(test[2:])
        plt.xlabel('Hours')
        plt.ylabel('Transaction Fees')
        plt.title('Transaction Fees (per block) per hour')
        plt.show()

s = slave(0,randint(5000,10000),2,1)
s.start()

from draw import *

test = [0] * 24
pre_t = "1/07/2017 0:00"

from datetime import timedelta, date


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


start_dt = date(2017, 7, 2)
end_dt = date(2017, 7, 31)
test = []
pre_t = "1/7/2017 0:00"
for dt in daterange(start_dt, end_dt):
    t = dt.strftime("%d/%m/%Y") + ' 0:00'
    test.append(s.query(pre_t, t))
    pre_t = t
print (test)
draw(test, 'transaction fees per day')


# # draw trends for a day # 16 is the critical point
# test = [0] * 24
# pre_t = "12/07/2017 0:00"
#
# for i in range(1, 24):
#     t = "12/07/2017 " + str(i) + ":00"
#
#     test[i] = s.query( pre_t,  t)
#     print(test[i], 'query from',  pre_t, ' to ', t)
#     pre_t = t
# from draw import *
# draw(test[1:])

# # draw trends for a year
# year = 2017
# list = [0] * 13
# pre_t = "1/1" + "/" + str(year) + " 00:00"
# for i in range(2, 13):
#     t = "1/" + str(i) + "/" + str(year) + " 00:00"
#     list[i] = s.query(pre_t, t)
#     pre_t = t
# from draw import *
# print (list)
# draw(list[1:])

# # draw trend for FX Fee in a day cumulating from a month
# test = [0] * 24
# pre_t = "1/07/2017 0:00"
# for j in range(2, 31):
#     for i in range(1, 24):
#         t = str(j) + "/07/2017 " + str(i) + ":00"
#
#         test[i] += s.query(pre_t, t)
#         print(test[i], 'query from', pre_t, ' to ', t)
#         pre_t = t
# from draw import *
# print (test)
# draw(test[1:])





#######################################
# # test a month
# month = 7
# year = 2017
# list = [0] * 30
# pre_t = "1/" + str(month) + "/" + str(year) + " 00:00"
# for i in range(2, 30):
#     t = str(i) + "/" + str(month) + "/" + str(year) + " 00:00"
#     list[i] = s.query(pre_t, t)
#     pre_t = t
# from draw import *
# print (list)



# # test a year
# year = 2017
# list = [0] * 13
# pre_t = "1/7" + "/" + str(year) + " 00:00"
# for i in range(8, 13):
#     t = "1/" + str(i) + "/" + str(year) + " 00:00"
#     print (t)
#     list[i] = s.query(pre_t, t)
#     pre_t = t
# from draw import *
# print (list)


# test a hour
#
# test = [0] * 60
# pre_t = "16/07/2017 6:00"
#
# for i in range(1, 60):
#     t = "16/07/2017 6:" + str(i)
#
#     test[i] = s.query( pre_t,  t)
#     print(test[i], 'query from',  pre_t, ' to ', t)
#     pre_t = t
# from draw import *
# draw(test[1:])



