import socket  # Import socket module
import threading
import pickle
import io
import sys
from random import randint
import time
import datetime

msgLength = 1024

def recvAll(socket, length):
    data = b''
    while True:
        packet = socket.recv(length)
        data += packet
        if len(packet) < length:
            return data

def sendAll(socket, data, length):
    cnt = length
    while cnt < len(data):
        # print(data[(cnt - length): cnt])
        socket.sendall(data[(cnt - length): cnt])
        cnt += length
    socket.sendall(data[(cnt - length): cnt])

#ports for communication between servers
receivePorts = [randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999)]
sendFromPorts  = [randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999)]



class slave(threading.Thread):

    def __init__(self, sid, Port):
        self.sid = sid
        self.message = ""
        self.Port = Port

        self.host = socket.gethostname()
        self.lock = threading.Lock()

        threading.Thread.__init__(self)


    def run(self):

        self.s = socket.socket()  # Create a socket object
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.Port))  # Bind to the clientPort
        self.s.listen(5)  # Now wait for client connection.
        while True:
            command, addr = self.s.accept()  # Establish connection with client.
            threading.Thread(target=self.on_new_command, args=(command, addr)).start()
        # print("exit!!!!")



    def on_new_client(self, clientM, addr):
        while True:
            msg = recvAll(clientM, msgLength)
            if (msg != b''):
                self.lock.acquire()
                file = io.BytesIO(msg)
                # print('Server', self.sid, 'receive from', addr, ' >> ', msg)
                while True:
                    if self.exitFlag:
                        break
                    try:
                        entry = pickle.load(file)
                        debug(entry)
                        if entry[0] == "stabilizeCenter":
                            self.stabilizeCenter(entry[1])
                            self.event.set()

                        elif entry[0] == "stabilizeSender":
                            self.stabilizeSender(entry[1])
                            self.event.set()

                        elif entry[0] == 'put':
                            self.update(entry[1:])
                            timeTuple = (self.vclock, self.vclock.getTimestamp(), self.sid)
                            sendAll(clientM, pickle.dumps(timeTuple), msgLength)
                            # clientM.sendall(pickle.dumps(timeTuple))

                        elif entry[0] == 'get':
                            valueTuple = self.get(entry[1:])
                            # print(pickle.dumps(valueTuple))
                            sendAll(clientM, pickle.dumps(valueTuple), msgLength)
                            # clientM.sendall(pickle.dumps(valueTuple))

                    except EOFError:
                        break

                self.lock.release()

    def update(self, insertTuple):
        """
        update writeLog and vClock, called when a write occurs
        insertTuple = (key, value, vclock)
        """
        self.updateItem(insertTuple)
        return 0

    def get(self, compTuple):
        """
        get value by checking wLog and history
        compTuple = (key, vclock, (sTime, sid))
        """
        # check wLog
        self.vclock.merge(compTuple[1])
        self.vclock.increment()
        key = compTuple[0]
        idx = len(self.writeLog) - 1
        while idx >= 0:
            if key == self.writeLog[idx][2][0]:
                value = self.writeLog[idx][2][1]
                curVersion = (self.writeLog[idx][0], self.writeLog[idx][1])
                return self.compVersion(value, curVersion, compTuple[2])
            else:
                idx -= 1
        # check history
        # if key in self.history:
        #     value = self.history[key][0]
        #     return self.compVersion(value, self.history[key][1:], tuple(compTuple[1]))
        return (self.vclock, 'ERR_KEY')

    def compVersion(self, value, curVersion, lastVersion):
        if curVersion[0] < lastVersion[0] or (curVersion[0] == lastVersion[0] and curVersion[1] < lastVersion[1]):
            return (self.vclock, "ERR_DEP")
        else:
            retTumple = (self.vclock, value, curVersion[0], curVersion[1])
            return retTumple

    def antiEntropy(self, otherLog, otherVclock):
        """
        Update wLog and vClock from exchanging with other server.
        writeLog = [(sTime, sid, (key, value))]
        """
        l1, l2 = len(self.writeLog), len(otherLog)
        merged = []
        i, j, total = 0, 0, 0
        while i < l1 and j < l2:
            if self.writeLog[i] > otherLog[j]:
                merged.append(otherLog[j])
                j += 1
            elif self.writeLog[i] == otherLog[j]:
                merged.append(otherLog[j])
                j += 1
                i += 1
            else:
                merged.append(self.writeLog[i])
                i += 1
        if i < l1:
            merged.extend(self.writeLog[i:])
        else:
            merged.extend(otherLog[j:])
        self.writeLog = merged
        del merged

        self.vclock.merge(otherVclock)

        # historyTime = min(self.vclock.vclock)
        # while len(self.writeLog) > 0 and self.writeLog[0][1] <= historyTime:
        #     key = self.writeLog[0][3][0]
        #     insertTuple = self.writeLog[0][3][1:] + (self.writeLog[0][1], self.writeLog[0][2])
        #     self.history[key] = insertTuple
        #     self.writeLog.pop()


    def updateItem(self, insertTuple):
        '''
        insertTuple = (key, value, vclock)
        '''
        self.vclock.merge(insertTuple[2])
        self.vclock.increment()
        newRow = (self.vclock.getTimestamp(), self.sid, insertTuple[0:2])
        self.writeLog.append(newRow)




    def sendWriteLog(self,toPort):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, sendFromPorts[self.sid]))
        s.connect((self.host, toPort))
        sendAll(s, pickle.dumps(("writeLog", self.writeLog, self.vclock)), msgLength)
        # s.sendall(pickle.dumps(("writeLog", self.writeLog, self.vclock)))
        return 0

    def receiveWriteLog(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host,receivePorts[self.sid]))
        s.listen(3)
        while True:
            msg, addr = s.accept()
            if self.exitFlag:
                break
            threading.Thread(target=self.on_otherWriteLog, args=(msg,) ).start()
        s.close()
        # print("exitReceive")




    def on_otherWriteLog(self,msg):
        self.receiveLock.acquire()
        a = recvAll(msg, msgLength)
        recvM = pickle.loads(a)
        self.antiEntropy(recvM[1], recvM[2])
        self.received = self.received +1
        self.receiveLock.release()



    def finish_receive(self, targetNum):
        while True:
            if self.received == targetNum:
                self.received = 0
                break

    '''
    We will receive the information from all connected servers and let the sid=0 server start
    '''
    def stabilizeCenter(self, connectedSids):

        self.finish_receive(len(connectedSids))
        for toSid in connectedSids:
            self.sendWriteLog(receivePorts[toSid])

    def stabilizeSender(self, centerSid):
        self.sendWriteLog(receivePorts[centerSid])
        self.finish_receive(1)
        #print(datetime.datetime.now())
