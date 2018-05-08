from initial import masterPort, recvAll, masterHost
import socket
import threading
import pickle
from random import randint
import io

Port = randint(3000, 9000)

def parse(msg):
    if (msg != b''):
        file = io.BytesIO(msg)
        while True:
            try:
                entry = pickle.load(file)
                print(entry)
                return entry
            except EOFError:
                break


#query_txFee_range
#query_topK_tx
#query_topK_addrs
#query_topK_pairs
def query(s,start,end):
    msg = pickle.dumps(("query_topK_pairs",start,end))
    s.sendall(msg)
    return parse(recvAll(s))



masterAddr = (masterHost, masterPort)

s=socket.socket()
s.bind((socket.gethostname(), Port))
s.connect(masterAddr)

######################################


from draw import *

from datetime import timedelta, date
import time

def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

print("GH")
print (query(s,"10/07/2017 20:00","11/07/2017 22:00"))
# # (1) transaction fees per day for a year
# start_dt = date(2017, 1, 1)
# end_dt = date(2017, 7, 31)
# test = []
# pre_t = "1/7/2017 0:00"
# x = []
# for dt in daterange(start_dt, end_dt):
#     t = dt.strftime("%d/%m/%Y") + ' 0:00'
#     test.append(query(s, pre_t, t))
#     print(test[-1], 'query from', pre_t, ' to ', t)
#     pre_t = t
#     x.append(dt.strftime("%d/%m/%Y"))
# print (test)
# draw_year(test, 'transaction fees per day',x)


#
# # (2) transaction fees per hour for a certain day
# test = [0] * 24
# pre_t = "12/07/2017 0:00"
#
# for i in range(1, 24):
#     t = "12/07/2017 " + str(i) + ":00"
#     test[i] = query(s, pre_t, t)
#     print(test[i], 'query from', pre_t, ' to ', t)
#     pre_t = t
# from draw import *
#
# draw(test[1:])

#(3) transaction fees per hour cumuating from a month

# start_dt = date(2017, 7, 9)
# end_dt = date(2017, 7, 11)
# test = [0] * 24
# count = 0
# start_time = time.time()
# for dt in daterange(start_dt, end_dt):
#     pre_t = dt.strftime("%d/%m/%Y") + ' 15:00'
#     for i in range(1, 24):
#         t = dt.strftime("%d/%m/%Y") + ' ' + str(i) +':00'
#         test[i] += (query(s, pre_t, t))
#         #print(test[-1], 'query from', pre_t, ' to ', t)
#         pre_t = t
#         count += 1
# end_time = time.time()
# print (test)
# todraw = [x / count for x in test][1:]
# print ((end_time - start_time)/count)
# print (todraw)
# draw(todraw, 'Average transaction fees per hour')
#
#
# # [DEMO UPDATE] draw trends for a hour
# test = [0] * 60
# pre_t = "16/07/2017 6:00"
#
# for i in range(1, 60):
#     t = "16/07/2017 6:" + str(i)
#
#     test[i] = query(s, pre_t,  t)
#     print(test[i], 'query from',  pre_t, ' to ', t)
#     pre_t = t
#
# draw(test[1:])


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
