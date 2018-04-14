import socket
import threading

import pickle


'''
lastOpDict = {key:(sTime, sid),}
'''

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
    socket.sendall(data[(cnt - length): len(data)])

class client(threading.Thread):

    def __init__(self, cid, cport, sport):
        threading.Thread.__init__(self)
        self.cid = cid
        self.cport = cport
        self.sport = sport

        self.host = socket.gethostname()
        self.addr = (self.host, self.cport)

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))

    def get(self, key):
        '''
        valueTuple = (vclock, value, sTime, sid)
        '''
        if not key in self.lastOpDict:
            self.lastOpDict[key] = (0, 0)
        sendAll(self.s, pickle.dumps(("get", key, self.vclock, self.lastOpDict[key])), msgLength)
        # self.s.sendall(pickle.dumps(("get", key, self.vclock, self.lastOpDict[key])))
        msg = recvAll(self.s, msgLength)
        # print(msg)
        # print(self.addr, "receive ", msg)
        valueTuple = pickle.loads(msg)
        self.vclock.merge(valueTuple[0])
        if valueTuple[1] == "ERR_DEP" or valueTuple[1] == "ERR_KEY":
            return valueTuple[1]
        else:
            self.lastOpDict[key] = (valueTuple[2], valueTuple[3])
            return valueTuple[1]


    def put(self, key, value):
        '''
        timeTuple = (vclock, sTime, sid)
        '''
        self.vclock.increment()
        insertTuple = ("put", key, value, self.vclock)
        sendAll(self.s, pickle.dumps(insertTuple), msgLength)
        msg = recvAll(self.s, msgLength)
        # print(self.addr, "receive ", msg)
        timeTuple = pickle.loads(msg)
        self.vclock.merge(timeTuple[0])
        self.lastOpDict[key] = (timeTuple[1], timeTuple[2])



    def connect(self, sport):
        self.sport = sport
        self.s.close()
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))

    def close(self):
        self.s.close()

    def run(self, status, arg0=None, arg1=None):
        if status == "query":
            self.query(arg0, arg1)



    def printError(self):
        print(self.cid)