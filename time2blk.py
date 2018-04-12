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


        self.map.extend([None]*s)
        self.size += s
        print ('size of map ', len(self.map))
        for i in range(s):
            idx =  offset + i - self.begin
            #print ("store idx ", idx, offset+i, " ts ", data[offset+i]["timestamp"] )
            self.map[idx] = data[offset+i]["timestamp"]
        f.close()

        print (self.map[0], self.map[900])
        return
    def getBlk(self, t):


        timestamp = time.mktime(datetime.datetime.strptime(t, "%d/%m/%Y %H:%M").timetuple())
        timestamp_int= int(timestamp)

        chk = timestamp_int
        if chk > self.map[self.size-1] or chk < self.map[0]:

            print ('error query. do not have data in this range')
            print ('Query ts is', chk, ', start from', self.map[0], '; end to:',  self.map[self.size-1])
            return
        res = self.binarySearch(0, self.size-1, chk)
        return res
    def binarySearch( self,l, r, x):

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
            # Element is not present in the array, choose l value
            return l
t = "30/01/2018 08:00"
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



#>>> time.ctime(data[5000900]['timestamp'])
#'Tue Jan 30 11:30:24 2018'
#>>> time.ctime(data[5000000]['timestamp'])
#'Tue Jan 30 07:41:33 2018'


#data[5000900]['timestamp']
#1517333424
#data[5000000]['timestamp']
#1517319693



