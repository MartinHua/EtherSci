
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class blkNode: # store block info
    def __init__(self, start, end, blk):
        #self.blockNum = blk["blockNum"]
        #self.miner = blk["miner"]
        #self.timestamp = blk["timestamp"]
        #self.gasUsed = blk["gasUsed"]
        #self.uncleReward = blk["uncleReward"]

        self.txFee = blk["txFee"]
        #self.reward = blk ["reward"]
        self.start = start
        self.end= end
        self.left = None
        self.right = None
        '''
        self.blockNum = tx["blockNum"]
        self.transactionIndex = tx["transactionIndex"]
        self.frm = tx["from"]
        self.to = tx["to"]
        self.value = tx["value"]
        self.gas = tx["gas"]
        self.gasPrice = tx["gasPrice"]
        self.data = tx["data"]
        '''


class blkSegTree(object):

    def __init__(self, blks, offset):
        self.offset = offset
        def buildTree(start, end, blks):
            if start >= end:
                return None
            if start + 1 == end:
                return blkNode(start, end, blks[start])
            root = blkNode(start, end, blks[self.offset]) #####????????????
            mid = int(start + (end - start) / 2)
            root.left = buildTree(start, mid, blks)
            root.right = buildTree(mid, end, blks)
            root.txFee = root.left.txFee + root.right.txFee

            return root

        self.root = buildTree(offset, offset+len(blks), blks)



    def query_txFee_Sum(self, i, j):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                return node.txFee
            mid = int(node.start + (node.end - node.start) / 2)
            return rangeHelper(i, min(j, mid), node.left) + rangeHelper(max(i, mid), j, node.right)

        return rangeHelper(i, j + 1, self.root)

    def inorder(self, root):
        if root == None:
            return
        self.inorder(root.left)
        print (root.start, root.end, root.txFee)
        self.inorder(root.right)
    def query_txFee_Max(self, i, j):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                return node.txFee
            mid = int(node.start + (node.end - node.start) / 2)
            return max(rangeHelper(i, min(j, mid), node.left),rangeHelper(max(i, mid), j, node.right))

        return rangeHelper(i, j + 1, self.root)
import pickle
filename = '5000000.p'
with open('/u/cchsu/Downloads/' + filename, 'rb') as f:
    data = pickle.load(f)

s= blkSegTree(data, 5000000)

#s.inorder(s.root)
case1 = 0
case2 = 1

if case1:
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
if case2:
    from time2blk import time2blk

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

'''
bs= []
for i in range(5):
    b = dict()
    #b["timestamp"] = 10-i
    b["txFee"] = i*10
    bs.append(b)
s= blkSegTree(bs)

s.inorder(s.root)
print (s.query_txFee_Sum(0, 3))
print (s.query_txFee_Max(0, 2))
'''