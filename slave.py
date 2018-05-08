import socket  # Import socket module
import threading
import pickle
import io
import sys
from random import randint
from time2blk import time2blk
from SegTree import *
from initial import *

#begin,offset, recvAll, sendAll, msgLength, script_dir,
#  masterListenFromSlaveAddr, updatePort, loadFileNum,fileBlockNum,queryPort


sendFromPort = randint(2602, 29999)



toStoreTotalBlockNum = fileBlockNum*loadFileNum

class slave(threading.Thread):

    def __init__(self, sid, Port, partition, precision):

        self.sid = sid
        self.message = ""
        self.Port = Port
        self.updatePort = updatePort
        self.begin = begin
        self.offset = offset
        self.host = socket.gethostname()

        self.sendToMasterSocket = socket.socket()
        self.sendToMasterSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sendToMasterSocket.bind((self.host, sendFromPort))
        print(masterListenFromSlaveAddr)
        self.sendToMasterSocket.connect(masterListenFromSlaveAddr)

        self.lock = threading.Lock()
        self.partition = partition
        # create a empty tree

        self.tree = blkSegTree(self.offset, treeSize)
        # offset (starting blk number), size of the tree

        self.mapping = time2blk(self.offset, mappingSize)
        # self.mapping.setBegin(self.offset)


        for i in range(loadFileNum):
            filename = str(self.offset) + '.p'
            if i % 100 == 99:
                print(i)
            try:
                with open(script_dir + filename, 'rb') as f:
                    blks = pickle.load(f)
                    blockLen = int(len(blks)/self.partition) + int(len(blks) % self.partition > self.sid)
                    for idx in range(blockLen):
                        blk = self.getBlock(blks, idx)
                        self.tree.update(blk)
                        self.mapping.update(blk["timestamp"])
                        self.maxBlock = blk["blockNum"]
                        self.maxTime = blk["timestamp"]
                    # self.mapping.buildMap(self.offset, filename)
                    self.offset += len(blks)
            except:
                print("No such file")
                break
        threading.Thread.__init__(self)
        threading.Thread(target=self.listen_new_block, args=()).start()
        print(self.maxBlock)
        self.sendBack("done", (self.maxBlock, self.maxTime))



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
                        # print(entry)
                        answer = self.query(entry[0], entry[2], entry[3])
                        # print(answer)
                        self.sendBack("answer", (entry[1], answer))
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

    def on_update_block(self, package):
        while True:
            rawblk = recvAll(package)
            blk = pickle.load(io.BytesIO(rawblk))
            self.tree.update(blk)
            self.mapping.update(blk["timestamp"])
            self.maxBlock = blk["blockNum"]
            self.maxTime = blk["timestamp"]
            self.sendBack("new", (blk["blockNum"], blk["timestamp"], blk["txFee"]))
            print(blk["blockNum"])

    def sendBack(self, msgType, msg=None):
        sendAll(self.sendToMasterSocket, pickle.dumps((msgType, self.sid, msg)), msgLength)
        return 0

    def query(self, queryType,startTime, endTime):
        try:
            # print(startTime, endTime)
            start = int(self.mapping.getBlk(startTime))
            end = int(self.mapping.getBlk(endTime))
            return eval("self.tree." + queryType +"(self.begin + start, self.begin + end)")
        except:
            print("Error")
            return -1.0


if len(sys.argv)>1:
    s = slave(*(eval(s) for s in sys.argv[1:]))
    s.start()
    # print('test', s.query("13/07 14:00", "13/07 15:00"))
else:
    s = slave(0, randint(5000, 10000), 1, 1)
    s.start()
    print('test', s.query("query","13/07 14:00", "13/07 15:00"))

