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

    def __init__(self, blks):

        def buildTree(start, end, blks):
            if start >= end:
                return None
            if start + 1 == end:
                return blkNode(start, end, blks[start])
            root = blkNode(start, end, blks[0]) #####????????????
            mid = start + (end - start) / 2
            root.left = buildTree(start, mid, blks)
            root.right = buildTree(mid, end, blks)
            root.txFee = root.left.txFee + root.right.txFee

            return root

        self.root = buildTree(0, len(blks), blks)



    def query_txFee_Sum(self, i, j):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                return node.txFee
            mid = node.start + (node.end - node.start) / 2
            return rangeHelper(i, min(j, mid), node.left) + rangeHelper(max(i, mid), j, node.right)

        return rangeHelper(i, j + 1, self.root)

    def query_txFee_Max(self, i, j):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                return node.txFee
            mid = node.start + (node.end - node.start) / 2
            return max(rangeHelper(i, min(j, mid), node.left),rangeHelper(max(i, mid), j, node.right))

        return rangeHelper(i, j + 1, self.root)


bs= []
for i in range(10):
    b = dict()
    b["timestamp"] = i
    b["txFee"] = i*10
    bs.append(b)
s= blkSegTree(bs)

print s.query_txFee_Sum(0, 3)
print s.query_txFee_Max(0, 3)