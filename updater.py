from parser import Parser
import threading
import socket
import pickle
import time
from random import randint
from initial import recvAll, sendAll, msgLength, slaveUpdateAddrs, slave_num
import os

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
            self.sendSockets = []
            for addr in addrs:
                s = socket.socket()
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((host, randint(30000, 40000)))
                s.connect(addr)
                self.sendSockets.append(s)

    def run(self):
        while self.updating:
            block = self.parser.getBlock(self.maxBlockNum)
            if block:
                if self.send:
                    message = pickle.dumps(block)
                    sendAll(self.sendSockets[self.maxBlockNum % slave_num], message)
                    print(slaveUpdateAddrs[self.maxBlockNum % slave_num])
                self.parser.saveBlock(block)
                self.maxBlockNum += 1
                print(self.maxBlockNum, self.maxFileNum)
                pickle.dump(self.parser.block, open(self.path + str(self.maxFileNum) + ".p", "wb"))
                if self.maxBlockNum % 1000 == 0:
                    self.parser.block = {}
                    self.maxFileNum += 1000
                    pickle.dump(self.parser.block, open(self.path + str(self.maxFileNum) + ".p", "wb"))
                    os.chmod(self.path + str(self.maxFileNum) + ".p", 0o777)
                with open(self.path + 'update.log', 'w') as f:
                    f.write(str(self.maxFileNum) + "\n")
                    f.write(str(self.maxBlockNum) + "\n")
                    f.close()
            else:
                time.sleep(5)
        return


if __name__ == "__main__":

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



