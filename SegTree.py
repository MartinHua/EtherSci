

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

        def countFeeBigger(th, blk):
            count = 0
            if blk == None:
                return 0
            #print (blk)
            for tx in blk['transactions']:
                if tx['txFee'] >= th*10**9:
                    count +=1
            return count
        def countFeeSmaller(th, blk):
            count = 0
            if blk == None:
                return 0
            #print (blk)
            for tx in blk['transactions']:
                if tx['txFee'] < th*10**9:
                    count +=1
            return count


        self.biggerThen1 = countFeeBigger(0.001, blk)
        self.smallerThen1 = countFeeSmaller(0.001, blk)
        self.numTx = len(blk['transactions'])
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
            root.biggerThen1 = root.left.biggerThen1 + root.right.biggerThen1
            root.smallerThen1 = root.left.smallerThen1 + root.right.smallerThen1
            root.numTx = root.left.numTx + root.right.numTx
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
        print (root.start, root.end, root.txFee, root.biggerThen1)
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

    def query_txFee_biggerThen1(self, i, j):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                return node.biggerThen1
            mid = int(node.start + (node.end - node.start) / 2)
            return rangeHelper(i, min(j, mid), node.left) + rangeHelper(max(i, mid), j, node.right)

        return rangeHelper(i, j + 1, self.root)
    def query_txFee_smallerThen1(self, i, j):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                return node.smallerThen1
            mid = int(node.start + (node.end - node.start) / 2)
            return rangeHelper(i, min(j, mid), node.left) + rangeHelper(max(i, mid), j, node.right)

        return rangeHelper(i, j + 1, self.root)
    def query_txFee_Num(self, i, j):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                return node.numTx
            mid = int(node.start + (node.end - node.start) / 2)
            return rangeHelper(i, min(j, mid), node.left) + rangeHelper(max(i, mid), j, node.right)

        return rangeHelper(i, j + 1, self.root)
'''
l = [ 8, 0, 5, 4, 3, 12, 18, 2, 1]
bs= []
for i in range(9):
    b = dict()
    #b["timestamp"] = 10-i
    b["txFee"] = l[i]
    bs.append(b)
s= blkSegTree(bs, 0)

s.inorder(s.root)
print (s.query_txFee_Sum(0, 8))
print (s.query_txFee_Max(0, 2))
print (s.query_txFee_biggerThen1(0, 8)
'''
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