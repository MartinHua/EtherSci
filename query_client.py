from initial import masterPort,recvAll
import socket
import threading
import pickle
from random import randint
import io

Port =  randint(3000, 9000)
def query(s,start,end):
    msg = pickle.dumps(("query",start,end))
    s.sendall(msg)

def parse(msg):
    if (msg != b''):
        file = io.BytesIO(msg)
        while True:
            try:
                entry = pickle.load(file)
                return entry
            except EOFError:
                break


masterAddr = (socket.gethostname(),masterPort)

s=socket.socket()
s.bind((socket.gethostname(), Port))
s.connect(masterAddr)

######################################




test = [0] * 24
pre_t = "12/07/2017 0:00"

for i in range(1, 24):
    t = "12/07/2017 " + str(i) + ":00"
    test[i] = query(pre_t, t)
    print(test[i], 'query from', pre_t, ' to ', t)
    pre_t = t
from draw import *

draw(test[1:])

# # draw trends for a year
# year = 2017
# list = [0] * 13
# pre_t = "1/1" + "/" + str(year) + " 00:00"
# for i in range(2, 13):
#     t = "1/" + str(i) + "/" + str(year) + " 00:00"
#     list[i] = query(s,pre_t, t)
#     pre_t = t
# from draw import *
#
# draw(list[1:])
#
# # draw trend for FX Fee in a day cumulating from a month
# test = [0] * 24
# pre_t = "1/07/2017 0:00"
# for j in range(2, 31):
#     for i in range(1, 24):
#         t = str(j) + "/07/2017 " + str(i) + ":00"
#
#         test[i] += query(s, pre_t, t)
#         print(test[i], 'query from', pre_t, ' to ', t)
#         pre_t = t
# from draw import *
#
# draw(test[1:])
# test = [0] * 24
# pre_t = "12/07/2017 0:00"
#
# for i in range(1, 24):
#     t = "12/07/2017 " + str(i) + ":00"
#     query(s,pre_t, t)
#     test[i] = parse(recvAll(s))
#     print(test[i], 'query from', pre_t, ' to ', t)
#     pre_t = t
# from draw import *
#
# draw(test[1:])
#
