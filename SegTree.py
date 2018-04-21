class blkNode:  # store block info
    def __init__(self, start, end, precision, blk=None):
        # self.blockNum = blk["blockNum"]
        # self.miner = blk["miner"]
        # self.timestamp = blk["timestamp"]
        # self.gasUsed = blk["gasUsed"]
        # self.uncleReward = blk["uncleReward"]

        # self.reward = blk ["reward"]
        self.start = start
        self.end = end
        self.left = None
        self.right = None
        self.txFee = 0
        self.precision = precision
        n = int(10 / self.precision)
        self.rangeTx = [0] * n
        self.numTx = 0
        if blk is not None:
            self.txFee = blk["txFee"]
            for i in range(n):
                self.rangeTx[i] = self.countRange(0.0001 * i * self.precision, 0.0001 * (i + 1) * self.precision, blk)
            self.numTx = len(blk['transactions'])

    def countRange(self, low, up, blk):
        count = 0
        if blk == None:
            return 0
        # print (blk)
        for tx in blk['transactions']:
            if tx['txFee'] < up * 10 ** 9 and tx['txFee'] >= low * 10 ** 9:
                count += 1
        return count




class blkSegTree(object):

    def __init__(self, offset, size):
        self.offset = offset
        self.filledID = 0
        self.precision = 10
        self.size = size
        def getNode(start, end, blks, precision):
            index = self.id + self.offset + self.partition * (start - self.offset)
            # print ('[debug] index: ', index, blks[index]["txFee"])
            return blkNode(start, end, precision, blks[index])

        def buildTree(start, end): # build an empty tree
            if start >= end:
                return None
            if start + 1 == end:
                return blkNode(start, end, self.precision)
            root = blkNode(start, end, self.precision)
            mid = int(start + (end - start) / 2)
            root.left = buildTree(start, mid)
            root.right = buildTree(mid, end)

            return root

        self.root = buildTree(offset, offset + size)
        # self.root = buildTree(offset, offset+ N, blks, precision)

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

    def update(self, blk):

        # update the whole path

        def updateHelper( blk, node):

            if node.start == self.filledID and node.end == self.filledID + 1:
                node.txFee = blk["txFee"]
                n = int(10 / self.precision)
                node.rangeTx = [0] * n
                for i in range(n):
                    node.rangeTx[i] = node.countRange(0.0001 * self.filledID * self.precision, 0.0001 * (self.filledID + 1) * self.precision,
                                                      blk)
                node.numTx = len(blk['transactions'])

                return
            mid = int(node.start + (node.end - node.start) / 2)
            if self.filledID < mid:
                updateHelper( blk, node.left)
            else:
                updateHelper(blk, node.right)
            node.txFee = node.left.txFee + node.right.txFee
            node.numTx = node.left.numTx + node.right.numTx
            node.rangeTx = [x + y for x, y in zip(node.left.rangeTx, node.right.rangeTx)]

        updateHelper(blk, self.root)
        self.filledID += 1
        assert (self.filledID <= self.size)
    def inorder(self, root):
        if root == None:
            return
        self.inorder(root.left)
        print(root.start, root.end, root.txFee)
        self.inorder(root.right)

    def query_txFee_Max(self, i, j):

        def rangeHelper(i, j, node):
            # return covered sum
            if node == None or i >= node.end or j <= node.start:
                return 0
            if i == node.start and j == node.end:
                return node.txFee
            mid = int(node.start + (node.end - node.start) / 2)
            return max(rangeHelper(i, min(j, mid), node.left), rangeHelper(max(i, mid), j, node.right))

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
                print('[debug] ', node.start, node.end, node.rangeTx)
                return count
            mid = int(node.start + (node.end - node.start) / 2)
            print('[debug] mid', mid)
            return rangeHelper(i, min(j, mid), node.left) + rangeHelper(max(i, mid), j, node.right)

        return rangeHelper(i, j + 1, self.root)


if __name__ == "__main__":
    # l = [ 8, 0, 5, 4, 3, 12, 18, 2, 1]
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    bs = []
    for i in range(10):
        b = dict()
        b["txFee"] = l[i]
        t = dict()
        t["txFee"] = 0.0005
        b["transactions"] = [t]
        bs.append(b)



    s1 = blkSegTree(0, 5)

    s1.inorder(s1.root)
    print('-----')

    s1.update(bs[0])
    s1.update(bs[1])
    s1.update(bs[2])
    s1.update(bs[3])
    s1.update(bs[4])
    print('-----')
    s1.inorder(s1.root)

