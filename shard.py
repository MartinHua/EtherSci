import socket
import threading
import os
import io
from random import randint
import sys
import pickle
import time





class Master(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print(socket.gethostname())
        self.queryNum = -1
        self.working = []
        self.answer = [0.]*1000
        self.answerNum = [[] for i in range(1000)]
        print(len(self.answerNum))
        print(self.answerNum)
        threading.Thread(target=self.listen_answer, args=()).start()
        time.sleep(0.1)
        os.system('bash slave.sh cchsu 10 ' + str(queryPort))
        while len(self.working) < 10:
            time.sleep(0.5)
        print("Done!")
        self.querySlaveSockets = []
        for addr in slaveAddrs:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((socket.gethostname(), randint(30000, 40000)))
            s.connect(addr)
            self.querySlaveSockets.append(s)

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
        for s in self.querySlaveSockets:
            message = pickle.dumps(("query", self.queryNum, start, end))
            s.sendall(message)
        print(self.queryNum)
        while True:
            if len(self.answerNum[self.queryNum]) == 10:
                return self.answer[self.queryNum]



if __name__ == "__main__":
    out = open("123.txt", "w")
    out.write(str(randint(4000,9000)))
    out.close()
    from initial import script_dir, slaveAddrs, masterListenFromSlaveAddr, recvAll, msgLength, queryPort

    master = Master()
    if len(sys.argv) > 1:
        master.query(*(eval(s) for s in sys.argv[1:]))

    test = [0] * 24
    pre_t = "12/07/2017 0:00"

    for i in range(1, 24):
        t = "12/07/2017 " + str(i) + ":00"
        test[i] = master.query(pre_t, t)
        print(test[i], 'query from', pre_t, ' to ', t)
        pre_t = t
    from draw import *

    draw(test[1:])


    # draw trends for a year
    year = 2017
    list = [0] * 13
    pre_t = "1/1" + "/" + str(year) + " 00:00"
    for i in range(2, 13):
        t = "1/" + str(i) + "/" + str(year) + " 00:00"
        list[i] = master.query(pre_t, t)
        pre_t = t
    from draw import *
    draw(list[1:])

    # draw trend for FX Fee in a day cumulating from a month
    test = [0] * 24
    pre_t = "1/07/2017 0:00"
    for j in range(2, 31):
        for i in range(1, 24):
            t = str(j) + "/07/2017 " + str(i) + ":00"

            test[i] += master.query(pre_t, t)
            print(test[i], 'query from', pre_t, ' to ', t)
            pre_t = t
    from draw import *

    draw(test[1:])