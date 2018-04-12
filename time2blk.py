import pickle
import time
import datetime

# this class helps to build a array where idx represent timestamp and value is the block number. idx = real_ - begin_ts
class time2blk: # store block info
    def __init__(self):
        self.map = []
        self.begin = 0
        self.size = 0
    def setBegin(self, offset):
        self.begin = offset

    def buildMap(self, offset, filename):
        with open('/u/cchsu/Downloads/' + filename, 'rb') as f:
            data = pickle.load(f)
        s = len(data)
        print('size  ', s)

        self.map.extend([None]*s)
        self.size += s
        print ('size of map ', len(self.map))
        for i in range(s):
            idx =  offset + i - self.begin
            print (idx)
            self.map[idx] = data[offset+i]["timestamp"]
        f.close()
    def getBlk(self, t):

        time_tuple = t.split("/")
        time_tuple =  [ int(x) for x in time_tuple ]
        time_tuple.extend((0, 0, 0, 0, 0, 0))
        #print (time_tuple)
        timestamp = time.mktime(tuple(time_tuple))
        timestamp_int= int(timestamp)
        #print (timestamp_int)
        #print (self.size)
        res = self.binarySearch(0, self.size-1, timestamp_int)
        return res
    def binarySearch( self,l, r, x):
        if x> self.map[r] or x < self.map[l]:
            print ('error query. do not have data in this range')
        # Check base case
        if r >= l:

            mid = l + int((r - l) / 2)

            # If element is present at the middle itself
            if self.map[mid] == x:
                return mid

            # If element is smaller than mid, then it
            # can only be present in left subarray
            elif self.map[mid] > x:
                return self.binarySearch(l, mid - 1, x)

            # Else the element can only be present
            # in right subarray
            else:
                return self.binarySearch( mid + 1, r, x)

        else:
            # Element is not present in the array
            return self.map[l]
t = "2018/1/22"
#getBlk(t, map)


filename = '5000000.p'
with open('/u/cchsu/Downloads/' + filename, 'rb') as f:
    data = pickle.load(f)
mapping = time2blk()
mapping.setBegin(5000000)
mapping.buildMap(5000000, '5000000.p')

print ( mapping.getBlk(t))

#print (data[5000000])
#t= data[5000000]["timestamp"]
#print (t)
#print (time.ctime(t))
