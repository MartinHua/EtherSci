
class blkNode: # store block info
    def __init__(self, start, end, precision, blk=None ):
        #self.blockNum = blk["blockNum"]
        #self.miner = blk["miner"]
        #self.timestamp = blk["timestamp"]
        #self.gasUsed = blk["gasUsed"]
        #self.uncleReward = blk["uncleReward"]


        #self.reward = blk ["reward"]
        self.start = start
        self.end= end
        self.left = None
        self.right = None


        def countRange(low, up, blk):
            count = 0
            if blk == None:
                return 0
            #print (blk)
            for tx in blk['transactions']:
                if tx['txFee'] < up*10**9 and tx['txFee'] >= low*10**9 :
                    count += 1
            return count
        self.txFee = 0
        n = int(10 / precision)
        self.rangeTx = [0] * n
        self.numTx = 0
        if blk is not None:
            self.txFee = blk["txFee"]
            for i in range(n):
                self.rangeTx[i] = countRange(0.0001*i*precision, 0.0001*(i+1)*precision, blk)
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

    def __init__(self, blks, offset, precision, id, partition):
        self.offset = offset
        self.id = id
        self.partition = partition
        self.precicion = precision
        def getNode(start, end, blks, precision):
            index = self.id + self.offset + self.partition*(start - self.offset)
            #print ('[debug] index: ', index)
            return blkNode(start, end,  precision, blks[index])
        def buildTree(start, end, blks, precision ):
            if start >= end:
                return None
            if start + 1 == end:
                return getNode(start, end, blks, precision)
            root = blkNode(start, end, precision)
            mid = int(start + (end - start) / 2)
            root.left = buildTree(start, mid, blks, precision)
            root.right = buildTree(mid, end, blks, precision)
            root.txFee = root.left.txFee + root.right.txFee
            root.numTx = root.left.numTx + root.right.numTx
            root.rangeTx = [x + y for x, y in zip(root.left.rangeTx, root.right.rangeTx)]
            #root.rangeTx = root.left.rangeTx + root.right.rangeTx
            return root
        #print('start: ', offset, ' end:', offset+ int(len(blks)/partition) )
        self.root = buildTree(offset, offset+ int(len(blks)/partition), blks, precision)



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
        print (root.start, root.end, root.rangeTx)
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
    def query_txFee_range(self, i, j, low, up):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                count = 0
                for x in range(low, up):
                    count += node.rangeTx[x]
                print ('[debug] ', node.start, node.end, node.rangeTx)
                return count
            mid = int(node.start + (node.end - node.start) / 2)
            print('[debug] mid', mid)
            return rangeHelper(i, min(j, mid), node.left) + rangeHelper(max(i, mid), j, node.right)

        return rangeHelper(i, j + 1, self.root)

#l = [ 8, 0, 5, 4, 3, 12, 18, 2, 1]
l = [0,1,2,3,4,5,6,7]
bs= []
for i in range(8):
    b = dict()
    #b["timestamp"] = 10-i
    b["txFee"] = l[i]
    t = dict()
    t["txFee"] = 0.0005
    b["transactions"] = [t]

    bs.append(b)
s1= blkSegTree(bs, 0, 1, 0, 2)

s2= blkSegTree(bs, 0, 1, 1, 2)
s1.inorder(s1.root)
print('-----')
s2.inorder(s2.root)
# print (s.query_txFee_Sum(0, 8))
# print (s.query_txFee_Max(0, 2))
# print (s.query_txFee_biggerThen1(0, 8)

'''
bs= []
for i in range(5):
    b = dict()
'''