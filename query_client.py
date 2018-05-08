from initial import masterPort, recvAll, masterHost
import socket
import threading
import pickle
from random import randint
import io
#
# Port = randint(3000, 9000)
#
# def parse(msg):
#     if (msg != b''):
#         file = io.BytesIO(msg)
#         while True:
#             try:
#                 entry = pickle.load(file)
#                 print(entry)
#                 return entry
#             except EOFError:
#                 break
#
#
# #query_txFee_range
# #query_topK_tx
# #query_topK_addrs
# #query_topK_pairs
# def query(s,start,end, type = 'query_txFee_Sum' ):
#     msg = pickle.dumps((type,start,end))
#     s.sendall(msg)
#     return parse(recvAll(s))
#
#
#
# masterAddr = (masterHost, masterPort)
#
# s=socket.socket()
# s.bind((socket.gethostname(), Port))
# s.connect(masterAddr)
#
# ######################################
#
#
from draw import *
#
# from datetime import timedelta, date
# import time

def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


# print("GH")
# print (query(s,"10/08/2017 20:00","11/08/2017 22:00", "query_txFee_range"))

# # (1) transaction fees per day for a year
# start_dt = date(2017, 7, 1)
# end_dt = date(2017, 12, 31)
# test = []
# pre_t = "1/7/2017 0:00"
# x = []
# for dt in daterange(start_dt, end_dt):
#     t = dt.strftime("%d/%m/%Y") + ' 0:00'
#     test.append(query(s, pre_t, t, 'query_txFee_Sum'))
#     print(test[-1], 'query from', pre_t, ' to ', t)
#     pre_t = t
#     x.append(dt.strftime("%d/%m/%Y"))
# print (test)
# draw_year(test, 'Transaction fees per day',x)


#
# (2) transaction fees per hour for a certain day
# test = [0] * 24
# pre_t = "19/01/2017 0:00"
#
# for i in range(1, 24):
#     t = "19/01/2017 " + str(i) + ":00"
#     test[i] = query(s, pre_t, t, 'query_txFee_Sum')
#     print(test[i], 'query from', pre_t, ' to ', t)
#     pre_t = t
# from draw import *
#
# draw(test[1:])

#(3) transaction fees per hour cumuating from a month

#
# start_dt = date(2017, 8, 1)
# end_dt = date(2017, 12, 31)
# test = [0] * 25
# test2 = [0] * 25
# count = 0
# start_time = time.time()
# for dt in daterange(start_dt, end_dt):
#
#     pre_t = dt.strftime("%d/%m/%Y") + ' 00:00'
#     for i in range(1, 25):
#         if i == 24:
#             t = dt.strftime("%d/%m/%Y") + ' ' + str(i-1) + ':59'
#         else:
#             t = dt.strftime("%d/%m/%Y") + ' ' + str(i) +':00'
#         test[i] += (query(s, pre_t, t, 'query_txFee_Sum'))
#         test2[i] += (query(s, pre_t, t, 'query_txFee_Num'))
#         #print(test[-1], 'query from', pre_t, ' to ', t)
#         pre_t = t
#         count += 1

import pickle

# with open('1', 'wb') as fp:
#     pickle.dump(test, fp)
# import pickle
#
# with open('2', 'wb') as fp2:
#     pickle.dump(test2, fp2)
test = pickle.load(open('1', 'rb'))
test2 = pickle.load(open('2', 'rb'))

test_Ave = [x/y for x, y in zip(test[1:], test2[1:])]
print (test)
# count = 3441343379510.837/0.9400842359013946
# todraw = [x / count /10**9 for x in test][1:]
# todraw2 = [x / count for x in test2][1:]
todraw3 = [x  /10**9 for x in test_Ave]

# print (todraw[1:])
# draw(todraw, 'Transaction fees per hour in 2017 ', 'Hours')
# draw(todraw2, 'Number of Transactions per hour in 2017 ', 'Hours')
draw(todraw3, 'Ave. Transaction fees per TX per hour in 2017 ', 'Hours')


# (4) Scattor Plot for Top K fees per month for 2017
#
# test = []
# pre_t = "1/7/2017 0:00"
# topK = 100
# x=[]
# from collections import Counter
# for i in range(8,13):
#     pre_t = "1/" + str(i) +'/2017 0:00'
#     for j in range (11, 32, 10):
#         t = str(j-1) + "/" + str(i) +'/2017 0:00'
#         res = query(s,pre_t, t, 'query_topK_tx')
#
#         if res == []:
#             test.append([0]*topK)
#         else:
#             res=[x[1]/10**9 for x in res]
#             res_sorted = sorted(res, reverse = True)
#             res_sorted = [x for x in res_sorted if x < 200]
#             test.append(res_sorted[:topK])
#         pre_t = t
#         x.append(str(i) + "/" + str(j-10))
# print (test)
# draw_scattor(test, 'Top 100 fees per 10 days in 2017', 'month', x)


#
# # (5) Average TX Fee per month for 2017
# test = []
# pre_t = "1/7/2017 0:00"
# topK = 100
# x=[]
# from collections import Counter
# for i in range(8,13):
#     pre_t = "1/" + str(i) +'/2017 0:00'
#     for j in range (11, 32, 10):
#         t = str(j-1) + "/" + str(i) +'/2017 0:00'
#         res = query(s,pre_t, t, 'query_topK_tx')
#
#         sum = query(s,pre_t, t, 'query_txFee_Sum')
#         num = query(s, pre_t, t, 'query_txFee_Num')
#         if num == 0:
#             test.append(0)
#         else:
#             test.append((sum / num)/10**9)
#         pre_t = t
#         x.append(str(i) + "/" + str(j - 10))
# print (x)
# print(test)
# draw(test, 'Average TX Fee per month in 2017','month',x)
#
# #
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

# (6) Top K active addrs per month for 2017

# test = []
# pre_t = "1/7/2017 0:00"
# topK = 100
# x=[]
# from collections import Counter
#
# for i in range(8,13):
#     pre_t = "1/" + str(i) +'/2017 0:00'
#     for j in range (11, 32, 10):
#         t = str(j-1) + "/" + str(i) +'/2017 0:00'
#         res = query(s,pre_t, t, 'query_topK_addrs')
#
#         if res == []:
#             test.append([0]*topK)
#         else:
#             tempList = Counter()
#             for k in range (len(res)):
#                 tmp = dict()
#                 tmp[res[k][0]]= int(res[k][1])
#                 tempList += Counter(tmp)
#             topKList = Counter(tempList).most_common(topK)
#             print ('test!!!', topKList)
#             topK_res = [x[1] for x in topKList]
#             topK_res = [x  for x in topK_res]
#             test.append(topK_res)
#         pre_t = t
#
#         x.append(str(i) + "/" + str(j - 10))
# print (test)
#
# draw_scattor(test, 'Top K active addrs per month for 2017', 'month', x, '# of transactions')

# (7) Top K active pairs per month for 2017
# pre_t = "11/07/2017 0:00"
# t = "12/07/2017 0:00"
# res = query(s, pre_t, t, 'query_topK_addrs')
# print (res)
# test = []
# pre_t = "1/7/2017 0:00"
# topK = 100
# x = []
# from collections import Counter
#
# for i in range(11, 13):
#     pre_t = "1/" + str(i) + '/2017 0:00'
#     for j in range(11, 32, 10):
#         t = str(j - 1) + "/" + str(i) + '/2017 0:00'
#         res = query(s, pre_t, t, 'query_topK_pairs')
#
#         if res == []:
#             test.append([0] * topK)
#         else:
#             tempList = Counter()
#             for k in range(len(res)):
#                 tmp = dict()
#                 tmp[res[k][0]] = int(res[k][1])
#                 tempList += Counter(tmp)
#             topKList = Counter(tempList).most_common(topK)
#             for l in range(len(topKList)):
#                 if topKList[l][1] > 80000:
#                     print('[peak]',pre_t, t, topKList[l])
#             topK_res = [x[1] for x in topKList]
#             topK_res = [x for x in topK_res]
#             test.append(topK_res)
#         pre_t = t
#
#         x.append(str(i) + "/" + str(j - 10))
# #print(test)
#
# draw_scattor(test, 'Top K active transaction pairs per 10 days', 'month', x, '# of transactions')

# pre_t = "11/10/2017 0:00"
# t = "21/10/2017 0:00"
# res = query(s,pre_t, t, 'query_topK_tx')
# print (sorted(res, key=lambda x: x[1], reverse = True))




# test = []
# pre_t = "1/7/2017 0:00"
# topK = 100
# x=[]
# from collections import Counter
#
# for i in range(8,13):
#     pre_t = "1/" + str(i) +'/2017 0:00'
#     for j in range (11, 32, 10):
#         t = str(j-1) + "/" + str(i) +'/2017 0:00'
#         res = [0]*9
#         for k in range(9):
#             res[k] = query(s, pre_t, t, 'query_txFee_range', k, k+1)
#
#         test.append(res)
#
#         pre_t = t
#
#         x.append(str(i) + "/" + str(j - 10))
# print (test)
#
#
# import seaborn as sns
# sns.set_style("whitegrid")
#
#
# for j in range(9):
#     plt.plot( test[j][1:24])
#
# plt.legend(['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10'])
# plt.xlabel('Hours')
# plt.ylabel('Numbers of Transaction')
# plt.title('Transaction Fees (per block) per hour (Range Query)')
# plt.show()
#

