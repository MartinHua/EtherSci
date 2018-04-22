from parser import Parser
import threading
import socket
import pickle
import time
from random import randint
from initial import recvAll, sendAll, msgLength

class Updater(threading.Thread):
    def __init__(self, path='/scratch/cluster/xh3426/etherData/', addrs=None):
        threading.Thread.__init__(self)
        self.path = path
        self.parser = Parser()
        self.updating = True
        self.maxBlockNum = 0
        self.send = False
        try:
            with open(self.path + 'update.log', 'r') as f:
                self.maxFileNum = int(f.readline())
                self.maxBlockNum = int(f.readline())
                f.close()
            self.parser.block = pickle.load(
                open(self.path + str(self.maxFileNum) + '.p', 'rb'))
        except:
            print("fail read temp data")
        if addrs:
            host = socket.gethostname()
            self.send = True
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((host, randint(30000, 40000)))
            for addr in addrs:
                self.s.connect(addr)

    def run(self):
        # num = 5000000
        # b = pickle.load(
        #     open(self.path + str(5000000) + '.p', 'rb'))
        while self.updating:
            block = self.parser.getBlock(self.maxBlockNum)
            # block = b[num]
            # time.sleep(0.1)
            if block:
                if self.send:
                    message = pickle.dumps(block)
                    sendAll(self.s, message)
                    # print(num)
                self.parser.saveBlock(block)
                self.maxBlockNum += 1
                print(self.maxBlockNum, self.maxFileNum)
                pickle.dump(self.parser.block, open(self.path + str(self.maxFileNum) + ".p", "wb"))
                if self.maxBlockNum % 1000 == 0:
                    self.parser.block = {}
                    self.maxFileNum += 1000
                with open(self.path + 'update.log', 'w') as f:
                    f.write(str(self.maxFileNum) + "\n")
                    f.write(str(self.maxBlockNum) + "\n")
                    f.close()
            else:
                time.sleep(5)
            # num += 1
        return


if __name__ == "__main__":
    slaveAddrs = [('idomeneo', 4000), ]
    updater = Updater(addrs=None)
    if updater.maxBlockNum > 0:
        updater.start()
    # time.sleep(10)
    # updater.updating = False
    # time.sleep(2)
    # if updater.is_alive():
    #     print("failed stop")
    # else:
    #     print("ok")



