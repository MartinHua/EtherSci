# easy version
import pickle
import pickle
import time
import datetime

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from time2blk import time2blk
from SegTree import *

t0 = time.time()
data = dict()
mapping = time2blk()
mapping.setBegin(4000000)
for i in range(50):
    num = 4000000 + i*1000
    filename = str(num) +'.p'
    with open('/u/cchsu/Downloads/EtherData-master/' + filename, 'rb') as f:
        temp = pickle.load(f)
        data.update(temp)
        mapping.buildMap(num, filename)
s = blkSegTree(data, 4000000)

t1 = time.time()

print ('p[here]', time.ctime(data[4000000]['timestamp']))
print ('p[here]', time.ctime(data[4019999]['timestamp']))
test = [0]*24
pre_b = 0
t2=time.time()
for i in range(24):
    t = "12/07/2017 " + str(i) + ":00"
    blk = mapping.getBlk(t)
    #print (blk)
    #print (pre_b, blk)
    test[i] = s.query_txFee_Sum(4000000+ pre_b, 4000000 + blk)
    pre_b = blk
t3=time.time()
print ("[time]" , (t1-t0) , (t3-t2)/24)
sns.set_style("darkgrid")
plt.plot(test[1:24])
plt.show()

for i in range(24):
    t = "11/07/2017 " + str(i) + ":00"
    blk = mapping.getBlk(t)
    print (blk)
    print (pre_b, blk)
    test[i] = s.query_txFee_Sum(4000000+ pre_b, 4000000 + blk)
    pre_b = blk
sns.set_style("darkgrid")
plt.plot(test[1:24])
plt.show()


case0 = 0
case01 = 0
case02 = 0
if case0:
    filename = '5000000.p'
    with open('/u/cchsu/Downloads/' + filename, 'rb') as f:
        data = pickle.load(f)

    s= blkSegTree(data, 5000000)

#s.inorder(s.root)


if case01:
    sum = [0]*900
    count = 0
    for i in range( 900):
        sum[i] = (s.query_txFee_Sum(5000000, 5000000+i))
        count += data[5000000+i]['txFee']
        print (sum[i], count)
    #print (s.query_txFee_Max(0, 2))


    sns.set_style("darkgrid")
    plt.plot(sum)
    plt.show()
if case02:


    mapping = time2blk()
    mapping.setBegin(5000000)
    mapping.buildMap(5000000, '5000000.p')
    test = [0]*30
    pre_b = 0
    for i in range(30):
        t = "30/01/2018 08:" + str(i*2)
        blk = mapping.getBlk(t)
        print (blk)
        print (pre_b, blk)
        test[i] = s.query_txFee_Sum(5000000+ pre_b, 5000000 + blk)
        pre_b = blk
    sns.set_style("darkgrid")
    plt.plot(test[1:30])
    plt.show()