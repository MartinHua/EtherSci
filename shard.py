import socket
import threading
import os
import io
from random import randint
import sys
import pickle
import time
from initial import script_dir, slaveAddrs, masterListenFromSlaveAddr, recvAll, msgLength


class Master(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.queryNum = -1
        self.working = []
        self.answer = [0.]*1000
        self.answerNum = [[None] for i in range(1000)]
        print(len(self.answerNum))
        print(self.answerNum)
        threading.Thread(target=self.listen_answer, args=()).start()
        time.sleep(0.1)
        os.system('bash slave.sh xh3426 10')
        while len(self.working) < 10:
            time.sleep(5)
        print("Done!")

    def listen_answer(self):
        listen = socket.socket()
        listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen.bind(masterListenFromSlaveAddr)
        listen.listen(12)
        while True:
            t, addr = listen.accept()
            threading.Thread(target=self.on_new_answer, args=(t,)).start()


    def on_new_answer(self, command):
        while True:
            msg = recvAll(command, msgLength)
            if (msg != b''):
                file = io.BytesIO(msg)
                while True:
                    try:
                        entry = pickle.load(file)
                        print(entry)
                        if entry[0] == "done":
                            self.working.append(entry[1])
                        elif entry[0] == "answer":
                            self.answerNum[entry[2]].append(entry[1])
                            self.answer[entry[2]] += entry[3]
                    except EOFError:
                        break

    def query(self, start, end):
        self.queryNum += 1
        for addr in slaveAddrs:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((socket.gethostname(), randint(30000, 40000)))
            s.connect(addr)
            message = pickle.dumps(("query", self.queryNum, start, end))
            s.sendall(message)
        print(self.queryNum)
        while True:
            if len(self.answerNum[self.queryNum]) == 10:
                return self.answer[self.queryNum]



if __name__ == "__main__":
    master = Master()
    if len(sys.argv) > 1:
        master.query(*(eval(s) for s in sys.argv[1:]))
    master.query(4000000, 4000999)
    master.query(4000000, 4000999)
    print(master.answerNum)