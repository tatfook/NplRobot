class AnimBlock():
    def __init__(self,ranges=[],times=[],data=[],type="Linear"):
        self.type = type
        self.ranges = ranges        
        self.times = times        
        self.data = data
    def reset(self):
        self.ranges = []        
        self.times = []        
        self.data = []
    def getDefaultValue(self):
        return self.data[0]
    def interpolateLinear(self,range,v1,v2):
        return  (v1 * (1.0 - range) + v2 * range)
    def getValue(self,anim,time):
        rangesCount = len(self.ranges)
        timesCount = len(self.times)
        dataCount = len(self.data)
        if(self.type != "NONE" and dataCount > 1):
            if(anim >=0 and anim < rangesCount):
                anim_range = self.ranges[anim]
            else:
                return self.data[0]
            if(anim_range[0] != anim_range[1]):
                pos = anim_range[0]
                nStart = anim_range[0]
                nEnd = anim_range[1]
                if(time >= self.times[nEnd]):
                    return self.data[nEnd]
                elif(time <= self.times[nStart]):
                    return self.data[nStart]

                pos = self.binarySearchForIndex(time,nStart,nEnd,self.times) or pos
                t1 = self.times[pos]
                t2 = self.times[pos+1]
                r = (time - t1) / (t2 - t1)
                vType = self.type
                if(vType == "Linear"):
                    return self.interpolateLinear(r, self.data[pos], self.data[pos+1])
                elif(vType == "Discrete"):
                    return self.data[pos]	
            else:
                return self.data[anim_range[0]]
        else:
            return self.data[0]
    def addKey(self,time,data):
        index = self.getNextKeyIndex(1,time)
    def binarySearchForIndex(self,value,nStart,nEnd,values):
        pos = None
        while(True):
            if(nStart >= nEnd):
                pos = nStart
                break
            if(((nStart + nEnd)%2) == 1 ):
                nMid = (nStart + nEnd - 1)/2
            else:
                nMid = (nStart + nEnd)/2
            nMid = int(nMid)
            startP = (values[nMid])
            endP = (values[nMid + 1])
                    
            if(startP <= value and value < endP ):
                pos = nMid
                break
            elif(value < startP ):
                nEnd = nMid
            elif(value >= endP):
                nStart = nMid+1
        return pos

    def getNextKeyIndex(self,anim,time):
        rangesCount = len(self.ranges)
        timesCount = len(self.times)
        dataCount = len(self.data)
        if(self.type != "NONE" and dataCount > 1):
            if(anim >=0 and anim < rangesCount):
                anim_range = self.ranges[anim]
            else:
                return
            if(anim_range[0] != anim_range[1]):
                pos = anim_range[0]
                nStart = anim_range[0]
                nEnd = anim_range[1]
                if(time >= self.times[nEnd]):
                    return nEnd
                pos = self.binarySearchForIndex(time,nStart,nEnd,self.times) or pos
                for i in range(pos-1, anim_range[0],-1):
                    if(self.times[i]>=time):
                        pos = i
                    else:
                        break
                return pos

        else:
            if((self.times[0] != None) and (self.times[0] >= time) ):
                return 0
        def setRangeByIndex(self,index,rangeFirst,rangeSecond):
            if(not self.ranges[index]):
                self.ranges[index] = []
            self.ranges[index] = [rangeFirst,rangeSecond]

#test_ranges = [
#    [0,4],
#]
#test_times = [
#    0,701,1501,2000,2501
#]
#test_data = [
#    1,0,1,1,1
#]
#anim_block = AnimBlock(test_ranges,test_times,test_data)
#print("index",anim_block.getNextKeyIndex(0,700),anim_block.getValue(0,700))
#print("index",anim_block.getNextKeyIndex(0,701),anim_block.getValue(0,701))
#print("index",anim_block.getNextKeyIndex(0,1500),anim_block.getValue(0,1500))
#print("index",anim_block.getNextKeyIndex(0,2501),anim_block.getValue(0,2501))
#print("index",anim_block.getNextKeyIndex(0,2502),anim_block.getValue(0,2502))