import socket  # Import socket module
import threading
import pickle
import io
import os
import sys
from random import randint
from time2blk import time2blk
from SegTree import *
import time
import datetime
from initial import recvAll, sendAll, msgLength, script_dir


# script_dir = os.path.dirname(os.path.dirname(__file__))+'/EtherData-master/'


updatePort = 4000

host = socket.gethostname()
sendToAddr = (host, updatePort)
offset = 4000000
filename = str(offset) + '.p'

with open(script_dir + filename, 'rb') as f:
        blks = pickle.load(f)
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, randint(30000, 40000)))
s.connect(sendToAddr)

for i in range(500):

    filename = str(offset) + '.p'
    with open(script_dir + filename, 'rb') as f:
        blks = pickle.load(f)
        # print ('open file', filename, 'check start data', blks[self.offset])
        sendAll(s, pickle.dumps(blks[offset + i]))
        time.sleep(0.5)
    offset += 1000







# # easy version
# import pickle
# import pickle
# import time
# import datetime
#
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# from time2blk import time2blk
# from SegTree import *
# import os
# p = 5
# # test sum. input is time
# t0 = time.time()
# data = dict()
# mapping = time2blk()
# mapping.setBegin(4000000)
# script_dir = os.path.dirname(os.path.dirname(__file__))+'/EtherData-master/'
# print(script_dir)
# for i in range(50):
#     num = 4000000 + i*1000
#     filename = str(num) +'.p'
#     with open(script_dir+filename, 'rb') as f:
#         temp = pickle.load(f)
#         data.update(temp)
#         mapping.buildMap(num, filename)
# s = blkSegTree(data, 4000000, p,0,1)
#
# t1 = time.time()
#
# print ('p[here]', time.ctime(data[4000000]['timestamp']), data[4000000]['timestamp'])
# print ('p[here]', time.ctime(data[4049999]['timestamp']),data[4049999]['timestamp'])
#
# test = [0]*24
# pre_b = 0
# t2=time.time()
# for i in range(24):
#     t = "12/07/2017 " + str(i) + ":00"
#     blk = mapping.getBlk(t)
#     #print (blk)
#     #print (pre_b, blk)
#     test[i] = s.query_txFee_Sum(4000000+ pre_b, 4000000 + blk)
#     pre_b = blk
# t3=time.time()
# print ("[time]" , (t1-t0) , (t3-t2)/24)
# sns.set_style("darkgrid")
# plt.plot(test[1:24])
# plt.xlabel('Hours')
# plt.ylabel('Transaction Fees')
# plt.title('Transaction Fees (per block) per hour')
# plt.show()
#
#
#
# # testS = [0]*24
# # testL = [0]*24
# # testT = [0]*24
# # for i in range(24):
# #     t = "12/07/2017 " + str(i) + ":00"
# #     blk = mapping.getBlk(t)
# #     #print (blk)
# #     #print (pre_b, blk)
# #     testT[i] = s.query_txFee_range(4000000+ pre_b, 4000000 + blk, 0, 6)
# #     testS[i] = s.query_txFee_range(4000000 + pre_b, 4000000 + blk, 0, 3)
# #     testL[i] = s.query_txFee_range(4000000 + pre_b, 4000000 + blk, 3, 6)
# #     pre_b = blk
# # t3=time.time()
# # print ("[time]" , (t1-t0) , (t3-t2)/24)
# # sns.set_style("darkgrid")
# # plt.plot( testT[1:24])
# # plt.plot( testS[1:24])
# # plt.plot( testL[1:24])
# # plt.legend(['[0.0001-0.0006]ETH', '[0.0001-0.0003]ETH', '[0.0003-0.0006]ETH'])
# # plt.xlabel('Hours')
# # plt.ylabel('Numbers of Transaction')
# # plt.title('Transaction Fees (per block) per hour (Range Query)')
# # plt.show()
#
# # #### test for precision 1
# # test = [[0]*24 for _ in range(9)]
# #
# # for i in range(24):
# #     t = "12/07/2017 " + str(i) + ":00"
# #     blk = mapping.getBlk(t)
# #     #print (blk)
# #     #print (pre_b, blk)
# #     for j in range(9):
# #         test[j][i] = s.query_txFee_range(4000000+ pre_b, 4000000 + blk, j, j+1)
# #     pre_b = blk
# # t3=time.time()
# # print ("[time]" , (t1-t0) , (t3-t2)/24)
# # sns.set_style("darkgrid")
# # for j in range(9):
# #     plt.plot( test[j][1:24])
# #
# # plt.legend(['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10'])
# # plt.xlabel('Hours')
# # plt.ylabel('Numbers of Transaction')
# # plt.title('Transaction Fees (per block) per hour (Range Query)')
# # plt.show()
# #
# # print ('Total num of Txansactions'+ str(s.query_txFee_Num(4000000, 4049999)))
#
#
# #### test for precision 5
#
# num = int(10/p)
# test = [[0]*24 for _ in range(num)]
#
# for i in range(24):
#     t = "12/07/2017 " + str(i) + ":00"
#     blk = mapping.getBlk(t)
#     #print (blk)
#     #print (pre_b, blk)
#     for j in range(num):
#         print(j)
#         test[j][i] = s.query_txFee_range(4000000+ pre_b, 4000000 + blk, j, j+1)
#     pre_b = blk
# t3=time.time()
# print ("[time]" , (t1-t0) , (t3-t2)/24)
# sns.set_style("darkgrid")
# for j in range(num):
#     plt.plot( test[j][1:24])
#
# plt.legend(['0-5', '5-10'])
# plt.xlabel('Hours')
# plt.ylabel('Numbers of Transaction')
# plt.title('Transaction Fees (per block) per hour (Range Query)')
# plt.show()
#
# print ('Total num of Txansactions'+ str(s.query_txFee_Num(4000000, 4049999)))
#
# # for i in range(24):
# #     t = "11/07/2017 " + str(i) + ":00"
# #     blk = mapping.getBlk(t)
# #     print (blk)
# #     print (pre_b, blk)
# #     test[i] = s.query_txFee_Sum(4000000+ pre_b, 4000000 + blk)
# #     pre_b = blk
# # sns.set_style("darkgrid")
# # plt.plot(test[1:24])
# # plt.show()
#
#
# case0 = 0
# case01 = 0
# case02 = 0
# if case0:
#     filename = '5000000.p'
#     with open('/u/cchsu/Downloads/' + filename, 'rb') as f:
#         data = pickle.load(f)
#
#     s= blkSegTree(data, 5000000)
#
# #s.inorder(s.root)
#
#
# if case01:
#     sum = [0]*900
#     count = 0
#     for i in range( 900):
#         sum[i] = (s.query_txFee_Sum(5000000, 5000000+i))
#         count += data[5000000+i]['txFee']
#         print (sum[i], count)
#     #print (s.query_txFee_Max(0, 2))
#
#
#     sns.set_style("darkgrid")
#     plt.plot(sum)
#     plt.show()
# if case02:
#
#
#     mapping = time2blk()
#     mapping.setBegin(5000000)
#     mapping.buildMap(5000000, '5000000.p')
#     test = [0]*30
#     pre_b = 0
#     for i in range(30):
#         t = "30/01/2018 08:" + str(i*2)
#         blk = mapping.getBlk(t)
#         print (blk)
#         print (pre_b, blk)
#         test[i] = s.query_txFee_Sum(5000000+ pre_b, 5000000 + blk)
#         pre_b = blk
#     sns.set_style("darkgrid")
#     plt.plot(test[1:30])
#     plt.show()
#