import socket  # Import socket module
import threading
import pickle
import io
import sys
from random import randint
from time2blk import time2blk
from SegTree import *
from initial import recvAll, sendAll, msgLength, script_dir, masterListenFromSlaveAddr, updatePort, loadFileNum,fileBlockNum,queryPort


sendFromPort = randint(2602, 29999)



toStoreTotalBlockNum = fileBlockNum*loadFileNum

class slave(threading.Thread):

    def __init__(self, sid, Port, partition, precision):

        self.sid = sid
        self.message = ""
        self.Port = Port
        self.updatePort = updatePort
        self.begin = 400000
        self.offset = 4000000
        self.host = socket.gethostname()

        self.sendToMasterSocket = socket.socket()
        self.sendToMasterSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sendToMasterSocket.bind((self.host, sendFromPort))
        print(masterListenFromSlaveAddr)
        self.sendToMasterSocket.connect(masterListenFromSlaveAddr)

        self.lock = threading.Lock()
        self.partition = partition
        # create a empty tree
        self.tree = blkSegTree(self.offset, 20000)
        # offset (starting blk number), size of the tree
        self.mapping = time2blk(self.offset, 200000)
        # self.mapping.setBegin(self.offset)


        for i in range(loadFileNum):
            filename = str(self.offset) + '.p'
            with open(script_dir + filename, 'rb') as f:
                blks = pickle.load(f)
                #print ('open file', filename, 'check start data', blks[self.offset])
                for idx in range(int(fileBlockNum/self.partition)):
                    self.tree.update(self.getBlock(blks, idx))
                self.mapping.buildMap(self.offset, filename)
            self.offset += fileBlockNum
            # print('current tree size', self.tree.size)
        threading.Thread.__init__(self)
        threading.Thread(target=self.listen_new_block, args=()).start()
        self.sendBack("done")




    def getBlock(self, blks, idx):
        index = self.sid + self.offset + idx * self.partition
        # print (idx, index, self.offset)
        # print (index, blks[index])
        try:
            return blks[index]
        except:
            return None


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
                        print(entry)
                        answer = self.query(entry[0], entry[2], entry[3])
                        print(answer)
                        self.sendBack(entry[0], entry[1], answer)
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
            print(blk["blockNum"])

    def sendBack(self, msgType, queryNum=None, answer=None):
        sendAll(self.sendToMasterSocket, pickle.dumps((msgType, self.sid, queryNum, answer)), msgLength)
        return 0

    def query(self, queryType,startTime, endTime):
        start = int(self.mapping.getBlk(startTime) / self.partition) #+ self.mapping.getBlk(startTime) % self.partition
        end = int(self.mapping.getBlk(endTime) / self.partition) # + self.mapping.getBlk(endTime) % self.partition)
        try:
            return eval("self.tree."+ queryType+"(self.begin + start, self.begin + end)")
        except:
            return -1
        #return self.tree.query_topK_addrs(self.begin + start, self.begin + end)


if len(sys.argv)>1:
    s = slave(*(eval(s) for s in sys.argv[1:]))
    s.start()
    # print('test', s.query(4000000, 4000100))
else:
    s = slave(0, randint(5000, 10000), 1, 1)
    s.start()
    print('test', s.query("query","13/07 14:00", "13/07 15:00"))

