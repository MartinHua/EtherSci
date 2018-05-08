import socket
import threading
import os
import io
from random import randint
import sys
import pickle
import time
import datetime

class Master(threading.Thread):

    def __init__(self, update=False):
        self.update = update
        threading.Thread.__init__(self)
        print(socket.gethostname())
        self.queryNum = -1
        self.working = []
        self.maxBlock = 0
        self.maxTime = 0
        threading.Thread(target=self.listen_answer, args=()).start()
        time.sleep(0.1)
        os.system('bash slave.sh xh3426 ' + str(slave_num) + ' ' + str(queryPort))
        while len(self.working) < slave_num:
            time.sleep(0.5)
        print("Done!")
        self.plot_initial()
        self.querySlaveSockets = []
        for addr in slaveAddrs:
            print(addr)
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((socket.gethostname(), randint(20000, 40000)))
            s.connect(addr)
            self.querySlaveSockets.append(s)
        self.answer = []
        self.answerNum = []

    def plot_initial(self):
        print(datetime.datetime.fromtimestamp(self.maxTime).strftime('%Y-%m-%d %H:%M:%S'))
        self.plot_initial_day = datetime.datetime.fromtimestamp(self.maxTime).strftime('%m/%d/%Y ')

        # datetime.datetime.fromtimestamp(
        #     int("1284101485")
        # ).strftime('%Y-%m-%d %H:%M:%S')
        #
        # for i in range(60):
        #     start
        #     self.query("query_txFee_range", )

    def plot_update(self, msg):
        print(msg)
        #  transaction fees per hour for a certain day
        test = [0] * 24
        #day = "12/07/2017 "
        pre_t = self.plot_initial_day + "0:00"

        for i in range(1, 24):
            t = self.plot_initial_day + str(i) + ":00"
            test[i] = self.query('query_txFee_Sum', pre_t, t)
            print(test[i], 'query from', pre_t, ' to ', t)
            pre_t = t
        #draw(test)
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
                        # print(entry)
                        msgType = entry[0]
                        msg = entry[2]
                        slaveId = entry[1]
                        if msgType == "done":
                            self.working.append(slaveId)
                            self.maxBlock = max(self.maxBlock, msg[0])
                            self.maxTime = max(self.maxTime, msg[1])
                        elif msgType == "answer":
                            if self.answerNum[msg[0]] == 0:
                                if type(msg[1]) == float:
                                    self.answer.append(0.0)
                                elif type(msg[1]) == int:
                                    self.answer.append(0)
                                else:
                                    self.answer.append([])
                            self.answerNum[msg[0]] += 1
                            if type(msg[1]) == type({}):
                                self.answer[msg[0]] += list(msg[1].items())
                                continue
                            self.answer[msg[0]] += msg[1]
                        elif msgType == "new":
                            self.plot_update(msg)
                    except EOFError:
                        break


    def on_new_query(self, command, addr):
        while True:
            msg = recvAll(command, msgLength)
            if (msg != b''):
                file = io.BytesIO(msg)
                while True:
                    try:
                        entry = pickle.load(file)
                        # print(entry)
                        # query type, start,end
                        if entry[0] == "get":
                            while self.answerNum[entry[2]-1] < slave_num:
                                time.sleep(0.5)
                            command.sendall(
                                pickle.dumps(self.answer[entry[1]:entry[2]])
                            )
                        else:
                            self.query(entry[0], entry[1], entry[2])
                    except EOFError:
                        break

    def query(self, queryType, start, end):
        self.queryNum += 1
        self.answerNum.append(0)
        for s in self.querySlaveSockets:
            message = pickle.dumps((queryType, self.queryNum, start, end))
            s.sendall(message)
        # print(self.queryNum)
        return self.queryNum
        # while True:
        #     if self.answerNum == 10:
        #         return self.answer

    def run(self):
        if self.update:
            from updater import Updater
            updater = Updater(addrs=slaveUpdateAddrs)
            updater.start()
        listen = socket.socket()
        listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen.bind((socket.gethostname(), masterPort))
        listen.listen(20)

        while True:
            t, addr = listen.accept()
            threading.Thread(target=self.on_new_query, args=(t, addr)).start()


if __name__ == "__main__":
    out = open("123.txt", "w")
    out.write(str(randint(4000, 9000)))
    out.close()
    print(int(open("123.txt", 'r').readline()))
    from initial import slave_num, masterPort, slaveAddrs, masterListenFromSlaveAddr, recvAll, msgLength, queryPort, slaveUpdateAddrs
    master = Master(update=False)
    master.start()
