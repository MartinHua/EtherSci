from parser import Parser
import threading
import socket
import pickle
import time
from shard import recvAll, sendAll, msgLength

slaveAddrs = [('falstaff', 4000)]
host = socket.gethostname()


class Updater(threading.Thread):
    def __init__(self, path='/scratch/cluster/xh3426/etherData/'):
        threading.Thread.__init__(self, slaveAddrs)
        self.path = path
        self.parser = Parser()
        self.updating = True
        self.maxBlockNum = 0
        try:
            with open(self.path + 'update.log', 'r') as f:
                self.maxFileNum = int(f.readline())
                self.maxBlockNum = int(f.readline())
                f.close()
            self.parser.block = pickle.load(
                open(self.path + str(self.maxFileNum) + '.p', 'rb'))
        except:
            print("fail read temp data")

        self.socket = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, randint(30000, 40000)))
        for addr in slaveAddrs:
            s.connect(addr)

    def run(self):
        while self.updating:
            block = self.parser.getBlock(self.maxBlockNum)
            if block:
                message = pickle.dumps(block)
                sendAll(self.s, message)
                self.parser.saveBlock(block)
                self.maxBlockNum += 1
                print(self.maxBlockNum, self.maxFileNum)
                if self.maxBlockNum % 10 == 0:
                    pickle.dump(self.parser.block,
                                open(self.path + str(self.maxFileNum) + ".p", "wb"))
                    if self.maxBlockNum % 1000 == 0:
                        self.parser.block = {}
                        self.maxFileNum += 1000
                    with open(self.path + 'update.log', 'w') as f:
                        f.write(str(self.maxFileNum) + "\n")
                        f.write(str(self.maxBlockNum) + "\n")
                        f.close()
            else:
                time.sleep(5)
        return


if __name__ == "__main__":
    updater = Updater()
    if updater.maxBlockNum > 0:
        updater.start()
    # time.sleep(10)
    # updater.updating = False
    # time.sleep(2)
    # if updater.is_alive():
    #     print("failed stop")
    # else:
    #     print("ok")
